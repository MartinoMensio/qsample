import glob
import gzip
import os
import subprocess
import shutil
import sys
import webbrowser


input_dir = 'input'
output_dir = 'output'
jar_path = 'target/qsample-0.1-jar-with-dependencies.jar'
output_html = 'quotes.html'


def clear_folders():
    shutil.rmtree(input_dir, ignore_errors=True)
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(input_dir)
    os.makedirs(output_dir)


def read_docs(path):
    with open(path) as f:
        return [l.strip() for l in f]


def write_docs(docs):
    print('reading %d examples' % len(docs))
    for i, doc in enumerate(docs):
        filename = '%02d.txt' % i
        with open(os.path.join(input_dir, filename), 'w') as f:
            f.write(doc)


def run_qsample():
    print('running qsample')
    cmd = 'java -jar %s --sample %s %s' % (
        jar_path, input_dir, output_dir)
    subprocess.call(cmd.split())


def parse_result(f):
    text = ''
    last_i_end = 0
    for line in f:
        try:
            token, i_beg, i_end, _, label = line.split()
        except:
            text += ' '
            continue
        token = token.decode("utf-8")
        label = label.decode("utf-8")
        i_beg, i_end = int(i_beg), int(i_end)
        if label == 'C':
            token = '<i>%s</i>' % token
        elif label == 'B':
            token = '<b>%s' % token
        elif label == 'E':
            token = '%s</b>' % token
        if i_beg > last_i_end:
            token = ' ' + token
        text += token
        last_i_end = i_end
    return text


def parse_results():
    print('parsing results')
    results = []
    for path in sorted(glob.glob('%s/*.quotations.gz' % output_dir)):
        with gzip.open(path, 'rb') as f:
            result = parse_result(f)
            results.append(result)
    with open(output_html, 'w') as f:
        f.write('<hr>'.join(results))
    print('wrote results to %s' % output_html)


def open_chrome():
    webbrowser.open_new_tab(output_html)


def main():
    docs = read_docs(sys.argv[1])
    clear_folders()
    write_docs(docs)
    run_qsample()
    parse_results()
    open_chrome()


if __name__ == '__main__':
    main()
