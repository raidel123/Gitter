import os
import subprocess
from subprocess import PIPE

repos = ["commons-math", "pdfbox"]
repoInfo = {}

def a():
    print "\ta:"
    a = subprocess.check_output('git rev-list --count HEAD', shell=True)
    a = a.rstrip('\n')
    print "\t\tTotal Number of Commits:", a
    return a

def b(commits):
    print "\tb:"

    # 1.b : average number of commits per file, per repo
    gitP = subprocess.Popen(('git ls-files'), shell=True, stdout=PIPE)
    fileCount = subprocess.check_output(('wc -l'), shell=True, stdin=gitP.stdout)
    fileCount = fileCount.rstrip('\n')
    gitP.wait()     # wait for subprocess to finish

    ret = float(commits) / float(fileCount)

    print "\t\tTotal Number of Files:", fileCount
    print "\t\tAverage Number of Commits Per File = %s / %s = %f" % (commits, fileCount, ret)

    return ret

def c():
    print "\tc:"

    # get a list of contributors email, one per line for each contributor
    # a couple of pipes to get each unique email, and sort the output
    # count the number of lines, total unique emails that contributed
    gitP = subprocess.Popen(('git log --pretty="%ae%n%ce"'), shell=True, stdout=PIPE)
    sortP = subprocess.Popen(('sort'), shell=True, stdin=gitP.stdout, stdout=PIPE)
    uniqP = subprocess.Popen(('uniq'), shell=True, stdin=sortP.stdout, stdout=PIPE)
    c = subprocess.check_output('wc -l', shell=True, stdin=uniqP.stdout)
    c = c.rstrip('\n')

    gitP.wait()
    sortP.wait()
    uniqP.wait()

    print "\t\tNumber of contributors:", c

    return c

def d(commits, contributors):
    print "\td:"

    # commits per contributor
    ret = float(commits) / float(contributors)

    # output
    print "\t\tAverage Number of Commits Per Contributor = %s / %s = %f" % (commits, contributors, ret)

    return ret

def e(commits):
    print "\te:"

    gitP = subprocess.check_output(('git shortlog -se'), shell=True)
    gitP = gitP[:-1]
    gitP = gitP.split('\n')

    contributors = {}

    for line in gitP:
        line = line.split('\t')
        #print line

        # TODO: IF git changes the output format of:
        # > git shortlog -se
        # Then the 3 assignments below, to parse output, need to be changed

        # get the number of commits for each Contributor
        a_commits = line[0].split(' ')[-1]

        # get the name for each Contributor
        # get the email for each Contributor
        a_name  = line[1].split('<')[0]
        a_email = line[1].split('<')[1].split('>')[0]

        #print a_commits
        #print a_name
        #print a_email

        # reduce by key, store sum of prev commits + new commits found
        if a_email in contributors.keys():
            sum = int(contributors[a_email][1]) + int(a_commits)
            contributors[a_email][1] = str(sum)
        else:
            contributors[a_email] = [a_name, a_commits]


    for author in contributors.keys():
        print   '\t\t' + contributors[author][0] + '\t' + author, \
                "{0:.3f}%".format(float(contributors[author][1])/float(commits) * 100)

    #print type(gitP)
    #print gitP
    #git shortlog -s --pretty="%ae"

    return contributors

def f():
    print "\tf:"

    print '\t\tAnswer Below in Combined Repo Answers'

def g():
    print "\tg:"

def h():
    print "\th:"

def i():
    print "\ti:"

def main():

    print "Question 1:"

    wd = os.getcwd()
    for repo in repos:

        repoInfo[repo] = []

        os.chdir(wd + '/' + repo)

        print "    Repo:", repo
        print ""

        # 1.a : overall number of commits, per repo
        #add result to dict
        a_ret = a()
        repoInfo[repo].append(('a', a_ret))

        print ""

        # 1.b : average number of commits per file, per repo
        #print fileCount
        b_ret = b(a_ret)
        repoInfo[repo].append(('b', b_ret))

        print ""

        # 1.c : number of contributors, per repos
        c_ret = c()
        print ""

        # 1.d : average number of commits per contributor, per repo
        d_ret = d(a_ret, c_ret)
        print ""

        # 1.e : percentage of changes done by each contributor, per repo
        e_ret = e(a_ret)
        print ""

        # 1.f : people that contributed to both projects, number of commits to each repo
        f_ret = f()
        print ""

        # 1.g : which contributors have been inactive for past six months or more, per repo
        g_ret = g()
        print ""

        # 1.h : number of files added,  deleted, modified in the past year, per repo
        h_ret = h()
        print ""

        # 1.i : summarize what was observed. Similarities, differences
        i_ret = i()
        print ""

        # cd back to calling directory

        # print answer lists for each repo
        # print repo + ":", repoInfo[repo]

        os.chdir(wd)

        '''
        os.chdir(dir)
        print os.listdir('.')
        os.chdir("..")
        print ""
        '''

if __name__ == "__main__":
    main();
