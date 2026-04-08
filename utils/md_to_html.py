import markdown


def make_post(md_file_path: str):
    with open(f'posts/{md_file_path}', 'r', encoding='utf-8') as file:
        if file:
            res = markdown.markdown(file.read())
        else:
            print('Could not read file')
    return res


if __name__ == '__main__':
    print(make_post('example.md'))
