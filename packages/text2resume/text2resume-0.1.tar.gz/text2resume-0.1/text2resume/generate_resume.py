import yaml
import re
import subprocess
import argparse
import os
import shutil

def load_yaml(yaml_file):
    with open(yaml_file, 'r') as file:
        return yaml.safe_load(file)

def replace_placeholders(template, data, prefix=''):
    if isinstance(data, dict):
        for key, value in data.items():
            template = replace_placeholders(template, value, prefix + key + '.')
    elif isinstance(data, list):
        for i, item in enumerate(data):
            if isinstance(item, dict):
                if 'experience' in prefix:
                    if not all([item.get('company'), item.get('title'), item.get('dates'), item.get('location')]):
                        continue
                elif 'projects' in prefix:
                    if not all([item.get('title'), item.get('date')]):
                        continue
            template = replace_placeholders(template, item, f"{prefix}{i}.")
        template = re.sub(r'\\resumeSubheading\s*{{{' + re.escape(prefix) + r'\d+\..*?}}}{.*?}\s*{.*?}{.*?}\s*\\resumeItemListStart.*?\\resumeItemListEnd', '', template, flags=re.DOTALL)
        template = re.sub(r'\\resumeItem\{{{' + re.escape(prefix) + r'\d+\..*?}}}\n?', '', template)
    else:
        escaped_value = re.sub(r'([&%$#_{}])', r'\\\1', str(data))
        placeholder = '{{' + prefix.rstrip('.') + '}}'
        template = re.sub(re.escape(placeholder), escaped_value, template)
    return template

def generate_tex(yaml_file, template_file, output_tex_file):
    data = load_yaml(yaml_file)
    with open(template_file, 'r') as file:
        template = file.read()
    final_content = replace_placeholders(template, data)
    with open(output_tex_file, 'w') as file:
        file.write(final_content)
    print(f"LaTeX content has been generated and written to {output_tex_file}")

def run_pdflatex(output_tex_file):
    subprocess.run(['pdflatex', f'{output_tex_file}'], check=True)

def move_files(output_tex_file, extras_folder, outputs_folder):
    base_name = os.path.splitext(output_tex_file)[0]
    output_pdf_file = base_name + '.pdf'
    if not os.path.exists(extras_folder):
        os.makedirs(extras_folder)
    if not os.path.exists(outputs_folder):
        os.makedirs(outputs_folder)
    if os.path.exists(output_pdf_file):
        destination = os.path.join(outputs_folder, os.path.basename(output_pdf_file))
        if os.path.exists(destination):
            os.remove(destination)
        shutil.move(output_pdf_file, destination)
    extensions_to_move = ['.aux', '.log', '.out', '.tex']
    for ext in extensions_to_move:
        file_to_move = base_name + ext
        if os.path.exists(file_to_move):
            destination = os.path.join(extras_folder, os.path.basename(file_to_move))
            if os.path.exists(destination):
                os.remove(destination)
            shutil.move(file_to_move, destination)
    print(f"Extra files have been moved to the {extras_folder} folder.")
    print(f"PDF file has been moved to the {outputs_folder} folder.")

def main():
    parser = argparse.ArgumentParser(description='Generate LaTeX resume from YAML data.')
    parser.add_argument('yaml_file', help='Path to the YAML data file')
    parser.add_argument('output_file', help='Name of the output LaTeX file')
    args = parser.parse_args()

    generate_tex(args.yaml_file, os.path.join(os.path.dirname(__file__), 'templates/template.tex'), args.output_file)
    run_pdflatex(args.output_file)
    move_files(args.output_file, 'generated-resumes/extras', 'generated-resumes/outputs')

if __name__ == '__main__':
    main()
