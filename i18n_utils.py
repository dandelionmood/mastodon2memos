import os
import subprocess

def run_command(command):
    """Run a shell command and print the output."""
    result = subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    print(result.stdout.decode())
    if result.stderr:
        print(result.stderr.decode())

def extract_strings():
    """Extract strings from Python files to a .pot file."""
    pot_file = 'locale/messages.pot'
    source_files = 'mastodon2memos/*.py mastodon2memos/commands/*.py mastodon2memos/clients/*.py'
    temp_pot_file = 'locale/temp_messages.pot'
    
    # Extract strings to a temporary .pot file
    command = f'xgettext -o {temp_pot_file} --language=Python --keyword=_ {source_files}'
    run_command(command)
    
    # Merge the temporary .pot file with the existing .pot file
    if os.path.exists(pot_file):
        command = f'msgmerge --update --backup=none {pot_file} {temp_pot_file}'
        run_command(command)
        os.remove(temp_pot_file)
    else:
        os.rename(temp_pot_file, pot_file)
    
    print(f'Strings extracted and updated in {pot_file}')

def create_po_file(locale):
    """Create or update a .po file for a specific locale."""
    pot_file = 'locale/messages.pot'
    po_file = f'locale/{locale}/LC_MESSAGES/messages.po'
    os.makedirs(os.path.dirname(po_file), exist_ok=True)
    
    if os.path.exists(po_file):
        # Merge the new .pot file with the existing .po file
        command = f'msgmerge --update --backup=none {po_file} {pot_file}'
    else:
        # Initialize a new .po file
        command = f'msginit --input={pot_file} --locale={locale} --output-file={po_file}'
    
    run_command(command)
    print(f'.po file created or updated at {po_file}')

def compile_mo_file(locale):
    """Compile a .po file to a .mo file."""
    po_file = f'locale/{locale}/LC_MESSAGES/messages.po'
    mo_file = f'locale/{locale}/LC_MESSAGES/messages.mo'
    command = f'msgfmt {po_file} --output-file={mo_file}'
    run_command(command)
    print(f'.mo file compiled at {mo_file}')

def main():
    extract_strings()
    locales = ['fr', 'de', 'es', 'it', 'pt', 'nl', 'pl', 'ru', 'cs', 'zh_CN', 'zh_TW', 'ja', 'ko'] 
    for locale in locales:
        create_po_file(locale)
        compile_mo_file(locale)

if __name__ == '__main__':
    main()