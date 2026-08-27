import os

def main():
    filepath = r"c:\Users\idhay\Desktop\RailTwin-Q\services\frontend_generator.py"
    if not os.path.exists(filepath):
        print(f"Error: file not found at {filepath}")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Repair the empty f-string brace syntax error
    content = content.replace("const coordinateHits = {};", "const coordinateHits = {{}};")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print("Success: Syntax error repaired in services/frontend_generator.py!")

if __name__ == "__main__":
    main()
