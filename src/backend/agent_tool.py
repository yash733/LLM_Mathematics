from langgraph.graph import StateGraph, START, END
from langchain_core.tools import Tool
from langchain_community.utilities import WikipediaAPIWrapper
import sympy as sp
from sympy import symbols, solve, diff, integrate, simplify, expand, factor
from src.schema import State
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode
import streamlit as st
from log.logger import logging

# ---- log --- #
log = logging.getLogger('Agent')
log.setLevel(logging.DEBUG)  #log

def wikipedia_tool(query):
    log.info(f'[wikipedia_tool] Query: {query}')  #log
    try:
        wikipedia_wrapper = WikipediaAPIWrapper()
        return wikipedia_wrapper.run(query)
    except Exception as e:
        log.error(f'[wikipedia_tool] Error: {e}')  #log

def sympy_calculator(expression):
    """
    Execute SymPy operations on mathematical expressions.
    
    Args:
        expression: A string containing a SymPy expression or operation
        
    Returns:
        String representation of the result
    """
    try:
        # Define common symbols
        x, y, z, t = symbols('x y z t')
        
        # Create a safe namespace for eval
        namespace = {
            'x': x, 'y': y, 'z': z, 't': t,
            'symbols': symbols,
            'solve': solve,
            'diff': diff,
            'integrate': integrate,
            'simplify': simplify,
            'expand': expand,
            'factor': factor,
            'sin': sp.sin,
            'cos': sp.cos,
            'tan': sp.tan,
            'exp': sp.exp,
            'log': sp.log,
            'sqrt': sp.sqrt,
            'pi': sp.pi,
            'E': sp.E,
            'oo': sp.oo,  # infinity
        }
        
        # Evaluate the expression
        result = eval(expression, {"__builtins__": {}}, namespace)
        """
        {"__builtins__": {}} --> Safe gaurd, from executing shell commands. BY making it = {} empty dict.
        
        Python normally provides ~150 built-in functions that are always available:
            File operations: open(), input()
            Code execution: exec(), eval(), compile()
            System access: __import__() (can import os, sys, etc.)
            Object inspection: dir(), vars(), globals()
            Common functions: print(), len(), str()
        """
        log.info(f'[sympy_calculator] Input: {expression} \tResult: {result}')  #log
        return str(result)
    except Exception as e:
        log.error(f'[sympy_calculator] Error: {e}')
        return f"Error: {str(e)}"

def get_tools():
    tools = [
        Tool(name='wikipedia',
            func=wikipedia_tool,
            description="A tool for searching the Internet to find the vatious information on the topics mentioned"),
        Tool(name='sympy',
            func=sympy_calculator,
            description="""Perform symbolic mathematics operations using SymPy.
                            Can solve equations, compute derivatives, integrals, simplify expressions, etc. 
                            Use standard SymPy syntax. Variables x, y, z, t are predefined.
                            Examples: 'solve(x**2 - 4, x)', 'diff(x**3 + 2*x, x)', 'integrate(x**2, x)'""")
            ]
    log.info(f'[get_tools] Tools: {tools}')
    return tools

def LLM(state: State)-> State:
    try:
        if not state.get('model'):
            log.error('[LLM] No model instance found in state')  #log
            return {'response': 'No model instance found. Please reconfigure.', 'messages': []}
        
        prompt = PromptTemplate(template="""
                                            Your a agent tasked for solving users mathemtical question. Break the question into smaller parts make use of looks.
                                            Logically arrive at the solution and provide a detailed explanation and display it point wise for the question below.
                                            Question:{question}
                                            Answer:                                
                                        """,
                                input_variables=['question']
                                )
        prompt_formatted = prompt.format(question=state.get('user_input'))
            
        tools = get_tools()
        model = state.get('model')
        model_with_tool = model.bind_tools(tools)
        
        if state.get('messages') and len(state['messages']) > 0:
            # Continue conversation with existing messages
            response = model_with_tool.invoke(state['messages'])
        else:
            # Start new conversation
            response = model_with_tool.invoke(prompt_formatted)

        log.info(f'[LLM] Response: {response}')
        return {'response':response, 'messages':[response]}     
    except Exception as e:
        log.error(f'[LLM] Error: {e}')

def custom_tool_node(state: State):
    try:
        if hasattr(state['messages'][-1], 'tool_calls') and state['messages'][-1].tool_calls:
            return "Tool_Node"
        else:
            return "Reset"
    except Exception as e:
        log.error(f'[custom_tool_node] Error: {e}')
        return "Reset"

def reset_messages(state: State):
    try:
        state['messages'] = []  # Reset just this field
        log.info('[reset_messages] State messages reset.')
        return state
    except Exception as e:
        log.error(f'[reset_messages] Error: {e}')
        return state
    
def graph():
    try:
        tools = get_tools()

        graph = (
            StateGraph(State)
            .add_node('LLM',LLM)
            .add_node('Tool_Node',ToolNode(tools))
            .add_node('Reset', reset_messages)

            .add_edge(START, 'LLM')
            .add_conditional_edges('LLM',custom_tool_node) # Tool_call Yes --> Tool_Node || NO --> END 
            .add_edge('Tool_Node','LLM')
            .add_edge('Reset', END)
            
            .compile(checkpointer = MemorySaver())
            )
        
        return graph
    except Exception as e:
        log.error(f'[graph] Error: {e}')