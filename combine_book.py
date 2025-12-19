# combine_book.py - For your split frontend/backend structure
import os

# Change this if your Markdown files are in a different folder inside frontend
book_folder = os.path.join("frontend", "docs")  # <-- Your book content

output = "my_book.txt"

print("Combining your Physical AI & Robotics book from frontend/docs/ ...\n")

count = 0
with open(output, "w", encoding="utf-8") as outfile:
    if not os.path.exists(book_folder):
        print(f"Error: Folder not found: {book_folder}")
        print("Check if 'frontend/docs/' exists and contains .md/.mdx files")
        exit()

    for root, dirs, files in os.walk(book_folder):
        # Skip hidden/system folders
        dirs[:] = [d for d in dirs if not d.startswith(".")]
        
        for file in files:
            if file.endswith((".md", ".mdx")) and not file.startswith("_"):
                path = os.path.join(root, file)
                relative_path = os.path.relpath(path, ".")
                print(f"[{count+1}] Adding: {relative_path}")
                count += 1
                
                outfile.write(f"\n\n{'='*100}\n")
                outfile.write(f"SECTION: {relative_path}\n")
                outfile.write(f"{'='*100}\n\n")
                
                try:
                    with open(path, "r", encoding="utf-8") as infile:
                        content = infile.read()
                        outfile.write(content.strip())
                        outfile.write("\n\n")
                except Exception as e:
                    print(f"   ⚠ Skipped {relative_path} (error: {e})")

print(f"\n✅ SUCCESS! Combined {count} Markdown files from your book.")
print(f"📄 Full text saved as: {output} (in project root)")
print(f"📏 Size: {os.path.getsize(output) / (1024*1024):.2f} MB")
print("\nNext step: Upload my_book.txt to your backend at http://127.0.0.1:8000/docs → POST /ingest/upload")