import ast
import re
import sys

def safe_eval(expression, globals_dict=None, locals_dict=None):
    try:
        tree = ast.parse(expression, mode='eval')
        
        if not is_safe_expression(tree.body):
            raise ValueError("Expression contains unsafe operations")
        
        code = compile(tree, '<string>', 'eval')
        return eval(code, globals_dict, locals_dict)
    except SyntaxError:
        raise ValueError(f"Invalid expression: {expression}")

def is_safe_expression(node):
    unsafe_types = (
        ast.Call,
        ast.Attribute,
        ast.Import,
        ast.ImportFrom,
        ast.Lambda,
    )
    
    for child in ast.walk(node):
        if isinstance(child, unsafe_types):
            return False
    
    return True

def patch_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pattern = r"eval\s*\(\s*(['\"])(.*?)\1\s*\)"
    
    def replacer(match):
        quote = match.group(1)
        expr = match.group(2)
        return f"ast.literal_eval({quote}{expr}{quote})"
    
    patched = re.sub(pattern, replacer, content)
    
    with open(filepath + '.patched', 'w', encoding='utf-8') as f:
        f.write(patched)
    
    print(f"✓ Patched file saved to {filepath}.patched")
    return patched

def replace_eval_with_literal_eval():
    import builtins
    
    original_eval = builtins.eval
    
    def wrapped_eval(expression, globals_dict=None, locals_dict=None):
        try:
            import ast
            result = ast.literal_eval(expression)
            return result
        except (ValueError, SyntaxError):
            return original_eval(expression, globals_dict, locals_dict)
    
    builtins.eval = wrapped_eval

if __name__ == "__main__":
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
        patch_file(filepath)
    else:
        print("Usage: python script.py <filepath>")
        print("\nOr use replace_eval_with_literal_eval() to patch at runtime")