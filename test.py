import glob
import gzip
import os
import subprocess
import shutil

docs = [
    '''“At its heart, politics isn’t about exchanges across these dispatch boxes, nor about eloquent speeches or media headlines. Politics is about the difference we make, every day, to the lives of people up and down this country. They are our reason for being here, and we should never forget it,” May told the Commons at PMQs.''',

    '''“Oh Whit my heart breaks for you. Sending you my love,” one Instagram user wrote.
“This is a topic that so rarely is talked about,” wrote another. “So many women experience miscarriages and we are felt alone because we think we are the only ones who have gone thru it.. thank you for bringing this up and being raw honest about it.”''',

    '''Ms Davidson also dismissed speculation that the Scottish Conservatives could become independent from the wider UK Conservative Party.
She said: "We are a devolved party, just as Scotland is devolved."
"As Scottish leader, I am in charge of policy, campaigning, staffing, funding, management, candidate selection and everything else that goes with fighting elections and communicating with voters."
"But my message is simple: not on my watch."''',

    '''Colin Clement, chairman of Stobswell Forum, said they are working with Dundee City Council to install the systems and that is what was causing the delay.''',

    '''Conservative MP Helen Whately, who raised the case, argued that flexible working should be the default position for all employees and should be added to all job adverts.''',

    '''Boris Johnson has claimed that "a sensible, pragmatic Brexit" will cement Scotland's place within the UK, as he sought to position himself as a firm defender of the Union while on a visit north of the Border.''',

    '''In a statement, the Official Receiver said he was "encouraged by the level of interest shown in purchasing British Steel" and that he was "now in further discussions with the potential buyers who have made the most viable offers for the business".''',

    '''The anti-abortion campaign group Both Lives Matter welcomed Hunt and Johnson's position because, it claimed, the majority in Northern Ireland "don't want abortion laws imposed by Westminster".'''
]
input_dir = 'input'
output_dir = 'output'
jar_path = 'target/qsample-0.1-jar-with-dependencies.jar'
output_html = 'quotes.html'


def clear_folders():
    shutil.rmtree(input_dir, ignore_errors=True)
    shutil.rmtree(output_dir, ignore_errors=True)
    os.makedirs(input_dir)
    os.makedirs(output_dir)


def write_docs():
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


def main():
    clear_folders()
    write_docs()
    run_qsample()
    parse_results()


if __name__ == '__main__':
    main()
