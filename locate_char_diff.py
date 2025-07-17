def compare_files_char_by_char(file1, file2):
    with open(file1, encoding="utf-8") as f1, open(file2, encoding="utf-8") as f2:
        content1 = f1.read()
        content2 = f2.read()

    min_len = min(len(content1), len(content2))

    for i in range(min_len):
        if content1[i] != content2[i]:
            start = max(i - 20, 0)
            context1 = content1[start:i]
            context2 = content2[start:i]
            print(f"❌ Różnica na pozycji {i}:")
            print(f"Kontekst (ostatnie 20 znaków):")
            print(f"  {file1}: '{context1}'")
            print(f"  {file2}: '{context2}'")
            print(f"Znak różniący się:")
            print(f"  {file1}: '{content1[i]}' (ord={ord(content1[i])})")
            print(f"  {file2}: '{content2[i]}' (ord={ord(content2[i])})")
            return

    if len(content1) != len(content2):
        print("⚠️ Pliki mają różne długości.")
        print(f"{file1}: {len(content1)} znaków")
        print(f"{file2}: {len(content2)} znaków")
        print(f"Pierwsza różnica na pozycji {min_len}:")
        print(f"  {file1}: '{content1[min_len:min_len+10]}'")
        print(f"  {file2}: '{content2[min_len:min_len+10]}'")
    else:
        print("✅ Pliki są identyczne znak po znaku.")

# Przykładowe użycie
compare_files_char_by_char("PBG_mod_1.txt", "PBG_mod_2.txt")
