import sys

def generate_adapter_template(name: str) -> str:
    class_name = f"{name}Adapter"
    return f"""
class {class_name}:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def request(self):
        # Translate the request to the adaptee's specific method
        return self.adaptee.specific_request()
"""

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python adapter_helper.py <AdapterName>")
        sys.exit(1)

    adapter_name = sys.argv[1]
    print(generate_adapter_template(adapter_name))
