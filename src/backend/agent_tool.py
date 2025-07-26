from langgraph.graph import StateGraph, START, END
from langchain_core.tools import Tool
from langchain.agents import Tool
from langchain_community.utilities import WikipediaAPIWrapper
import sympy as sp
from sympy import symbols, solve, diff, integrate, simplify, expand, factor
from src.schema import State
from langchain_core.prompts import PromptTemplate
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import tools_condition, ToolNode

def wikipedia_tool(query: str):
    wikipedia_wrapper = WikipediaAPIWrapper()
    return wikipedia_wrapper.run(query)

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
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"

def tool_node():
    tools_ = [
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
    return tools_

def LLM(state: State):
    prompt = PromptTemplate(template="""
                                        Your a agent tasked for solving users mathemtical question. Logically arrive at the solution and provide a detailed explanation
                                        and display it point wise for the question below
                                        Question:{question}
                                        Answer:                                
                                    """,
                            input_variables=['question']
                            )
    prompt_=prompt.format(question=state.get['user_input'])
    tools_ = tool_node()
    model_with_tool = state.model.bind_tools(tools_, parallel_tool_calls = False)
    response = model_with_tool.invoke(prompt_)

    return {'response':response, 'message_history':response}     

def graph(state: State):
    tool_ = tool_node()
    graph = (
        StateGraph(state)
        .add_node('LLM',LLM)
        .add_node('Tool_Node',ToolNode(tool_))

        .add_edge(START, 'LLM')
        .add_conditional_edges('LLM',tools_condition) # Tool_call Yes --> Tool_Node | NO --> END 
        .add_edge('Tool_Node','LLM')
        
        .compile(checkpointer = MemorySaver())
        )
    
    return graph