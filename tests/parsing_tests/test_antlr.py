from eco_profiles.parse_profiles import parse_profile_string, ProfileExtractor


def generate_antlr_test(file_path, target_file):
    with open(file_path, 'r', encoding='utf8') as test_file, open(target_file, 'w', encoding='utf8') as out_file:
        diffs = 0
        while True:
            try:
                profile = next(test_file).strip()
                ref = next(test_file).strip()
                paraphrase = next(test_file).strip()
            except Exception:
                break
            tree, parser = parse_profile_string(profile)
            flat = tree.toStringTree(recog=parser).strip()
            if flat != ref:
                diffs += 1
                print(f'Expected: {ref}')
                print(f'Actual  : {flat}')
            out_file.write(profile)
            out_file.write('\n')
            out_file.write(flat)
            out_file.write('\n')
            extractor = ProfileExtractor()
            actual_paraphrase = extractor.visit(tree).describe()
            if actual_paraphrase != paraphrase:
                diffs += 1
                print(f'***** Paraphrase error for: {profile}')
                print(f'Expected: {paraphrase}')
                print(f'Actual  : {actual_paraphrase}')
            out_file.write(actual_paraphrase)
            out_file.write('\n')
    print(f'Total errors: {diffs}')


def test_antlr_file(file_path):
    errs = 0
    with open(file_path, 'r', encoding='utf8') as test_file:
        while True:
            try:
                profile = next(test_file).strip()
                ref = next(test_file).strip()
                paraphrase = next(test_file).strip()
            except Exception:
                break
            tree, parser = parse_profile_string(profile)
            flat = tree.toStringTree(recog=parser).strip()
            if flat != ref:
                errs += 1
                print(f'***** Parsing error for: {profile}')
                print(f'Expected: {ref}')
                print(f'Actual  : {flat}')
            extractor = ProfileExtractor()
            actual_paraphrase = extractor.visit(tree).describe()
            if actual_paraphrase != paraphrase:
                errs += 1
                print(f'***** Paraphrase error for: {profile}')
                print(f'Expected: {paraphrase}')
                print(f'Actual  : {actual_paraphrase}')
    print(f'Total errors: {errs}')


if __name__ == '__main__':
    # test_antlr_file(r'D:\Yishai\ws\eco\Profile-Parser\data\test-profiles.txt')
    generate_antlr_test(r'../../../../eco/Profile-Parser/data/test-profiles.txt',
                        r'../../../../eco/Profile-Parser/data/test-profiles-new.txt')
