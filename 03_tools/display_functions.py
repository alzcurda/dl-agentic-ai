from IPython.display import display, HTML
import json

def pretty_print_chat_completion(response):
    """
    A basic display function to render the response from aisuite.
    """
    html_content = ""
    tool_sequence = []
    
    # We inspect the final response choice
    choice = response.choices[0]
    message = choice.message
    
    # If the response contains tool calls (when manual handling is used)
    if getattr(message, "tool_calls", None):
        for tool_call in message.tool_calls:
            tool_name = tool_call.function.name
            
            try:
                # Try to parse and format JSON arguments nicely
                args_parsed = json.loads(tool_call.function.arguments)
                tool_args = json.dumps(args_parsed, indent=2)
            except:
                tool_args = tool_call.function.arguments
                
            tool_sequence.append(tool_name)
            
            html_content += f"""
            <div style="border-left: 4px solid #444; margin: 10px 0; padding: 10px; background: #f0f0f0;">
                <strong style="color:#222;">🧠 LLM Action:</strong> <code>{tool_name}</code>
                <pre style="color:#000; font-size:13px;">{tool_args}</pre>
            </div>
            """
    
    # Render final message content
    if message.content:
        html_content += f"""
        <div style="border-left: 4px solid #28a745; margin: 20px 0; padding: 10px; background: #eafbe7;">
            <strong style="color:#222;">✅ Final Assistant Message:</strong>
            <p style="color:#000;">{message.content}</p>
        </div>
        """
        
    # Render tool sequence summary if tools were used
    if tool_sequence:
        seq_str = " &rarr; ".join(tool_sequence)
        html_content += f"""
        <div style="border-left: 4px solid #666; margin: 20px 0; padding: 10px; background: #f8f9fa;">
            <strong style="color:#222;">🧭 Tool Sequence:</strong>
            <p style="color:#000;">{seq_str}</p>
        </div>
        """
        
    display(HTML(html_content))
