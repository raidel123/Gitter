import os
import subprocess
import git
import json
import itertools
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np

from subprocess import PIPE
from datetime import date, datetime, timedelta

homePath = os.getcwd()
repos = [ "commons-math", "pdfbox"]
repoInfo = {}
reposChanges = {}

def aa():
    print "\t\ta)"
    a = subprocess.check_output('git rev-list --count HEAD', shell=True)
    a = a.rstrip('\n')
    print "\t\t\tTotal Number of Commits:", a
    return a

def b(commits):
    print "\t\tb)"

    # 1.b : average number of commits per file, per repo
    gitP = subprocess.Popen(('git ls-files'), shell=True, stdout=PIPE)
    fileCount = subprocess.check_output(('wc -l'), shell=True, stdin=gitP.stdout)
    fileCount = fileCount.rstrip('\n')
    gitP.wait()     # wait for subprocess to finish

    ret = float(commits) / float(fileCount)

    print "\t\t\tTotal Number of Files:", fileCount
    print "\t\t\tAverage Number of Commits Per File = %s / %s = %f" % (commits, fileCount, ret)

    return ret

def c():
    print "\t\tc)"

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

    print "\t\t\tNumber of contributors:", c

    return c

def d(commits, contributors):
    print "\t\td)"

    # commits per contributor
    ret = float(commits) / float(contributors)

    # output
    print "\t\t\tAverage Number of Commits Per Contributor = %s / %s = %f" % (commits, contributors, ret)

    return ret

def e(commits):
    print "\t\te)"

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

    template = "{0:25}{1:25}\t{2:20}" # column widths: 50, 50, 20
    print "\t\t\t" + template.format("Contributor Name", "Contributor Email", "Percent of Commits")
    print ""
    for author in contributors.keys():
        print "\t\t\t" + template.format(contributors[author][0][0:25], author[0:25], "{0:.3f}%".format(float(contributors[author][1])/float(commits) * 100))

    return contributors

def f():
    print "\t\tf)"

    print '\t\t\tAnswer Below in Common Repo Answers'

def g(repo, contributors):
    print "\t\tg)"

    print "\t\t\tContributors Inactive For More Than 6 Months:"
    inactiveTime = 30 * 6        # 30 days per month, for 6 months
    today = datetime.today()
    afterDate = today - timedelta(days=inactiveTime)

    #print afterDate.date()
    g = git.Git(getPath(repo))
    logInfo = g.log('--after={' + str(afterDate.date()) + '}', '--pretty=format:"%ae"')
    logToList = str(logInfo).split('\n')

    # remove duplicates
    logToList = list(set(logToList))
    for i, val in enumerate(logToList):
        logToList[i] = val.strip('"')
        #print "\t\tLog", val

    #print logToList

    for author in contributors:
        if author not in logToList:
            print "\t\t\t" + author

     # git log --after={2017-08-01} --pretty=format:"%ae" | sort | uniq

def h(repo):
    print "\t\th)"

    g = git.Git(getPath(repo))

    #gitP = subprocess.Popen(('git log --pretty=format:"" --diff-filter=A --summary'), shell=True, stdout=PIPE)
    #diffP = subprocess.Popen(('grep create'), shell=True, stdin=gitP.stdout, stdout=PIPE)
    #c = subprocess.check_output('wc -l', shell=True, stdin=diffP.stdout)
    #c = c.strip('\n')

    #gitP.wait()
    #diffP.wait()

    logInfo = g.log('--pretty=format:""', '--diff-filter=A', '--summary', '--since="1 year ago"')
    logToList = logInfo.split('\n')

    #for log in logToList:
        #print log

    #print "size:", len(logToList)
    for i, val in enumerate(logToList):
        logToList[i] = str(val).strip('"')
    #print logToList

    createNum = 0
    for log in logToList:
        if "mode" in log:
            createNum += 1

        # print the lines that are obtained from the log query
        # print log

    #print "log size:", len(logToList)
    print "\t\t\tNumber Of Files Added:", createNum

    logInfo = g.log('--pretty=format:""', '--diff-filter=D', '--summary')
    logToList = logInfo.split('\n')

    for i, val in enumerate(logToList):
        logToList[i] = str(val).strip('"')

    deleteNum = 0
    for log in logToList:
        if "delete" in log:
            deleteNum += 1

        # print the lines that are obtained from the log query
        # print log

    #print "log size:", len(logToList)
    print "\t\t\tNumber Of Files Deleted:", deleteNum

    logInfo = g.log('--pretty=format:tformat', '--diff-filter=M')
    #print logInfo
    logToList = str(logInfo).split('\n')

    #for log in logToList:
        #print log

    modifyNum = len(logToList)

        # print the lines that are obtained from the log query
        # print log

    #print "log size:", len(logToList)
    print "\t\t\tNumber Of Files Modified:", modifyNum


    # git log --pretty=format:"" --diff-filter=A --summary | grep create | wc -l
def ii():
    print "\t\ti)"
    print '\t\t\tAnswer Below in Common Repo Answers'

def getHashes():
    hashes = subprocess.check_output('git log --pretty=format:"%h"', shell=True)
    hashes = hashes.split('\n')

    #print "hashes:", hashes
    return hashes

def changedFiles(repo, hashes):
    changes = []

    for hash in hashes:
        #print hash
        files = subprocess.check_output(('git diff-tree --no-commit-id --name-only -r ' + hash), shell=True)
        files = files.split('\n')
        files = files[:-1]                          # remove empty space at end of every line
        if len(files) > 0:
            # print files
            changes.append(files)
        #print ""

        # bottom line is done in main with return
        #reposChanges[repo] = changes

    return changes

def getPath(repo):
    return homePath + '/' + repo

def main():

    print "Question 1:"
    print ""

    contributors = {}

    for repo in repos:

        repoInfo[repo] = []

        os.chdir(getPath(repo))
        print "\tRepo:", repo
        print ""

        # 1.a : overall number of commits, per repo
        #add result to dict
        a_ret = aa()
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
        e_ret = e(a_ret)    # return a list  of contributors
        contributors[repo] = e_ret
        print ""

        # 1.f : people that contributed to both projects, number of commits to each repo
        f_ret = f()
        print ""

        # 1.g : which contributors have been inactive for past six months or more, per repo
        g_ret = g(repo, e_ret)
        print ""

        # 1.h : number of files added,  deleted, modified in the past year, per repo
        h_ret = h(repo)
        print ""

        # 1.i : summarize what was observed. Similarities, differences
        i_ret = ii()
        print ""

        # cd back to calling directory

        # print answer lists for each repo
        # print repo + ":", repoInfo[repo]

        os.chdir(homePath)
        print "\n"

    # 1.f : people that contributed to both projects, number of commits to each repo
    print "\tCommon Questions for %s and %s :" % (repos[0], repos[1])
    print ""

    print "\t\tf. Authors That Contributed to Both Projects:"

    found = False
    for author in contributors[repos[0]]:
        if author in contributors[repos[1]]:
            found = True
            print "\t\t" + author

    if not found:
        print "\t\t\tNone Found"

    print ""
    # 1.h : number of files added,  deleted, modified in the past year, per repo
    print "\t\ti : summarize what was observed. Similarities, differences:"
    print   "\t\t\tObserving the results for both repositories showed that just because both repositories belong to apache, it doesn't mean that developers in one project will necessarily contribute to another project. I also observed that only a few developers are typically responsible for the majority of commits in the project. Most contributos are also typically inactive after a certain period of time since the project was released. After some time only a few contributors continue to push commits, therefore only a few maintain the software."

    print '\n'



    print "Question 2:"
    print ""

    '''
    changes = []

    for repo in repos:
        os.chdir(getPath(repo))

        hashes = getHashes()
        changes = changedFiles(repo, hashes)
        reposChanges[repo] = changes

        os.chdir(homePath)

    with open('data.json', 'w') as outfile:
        json.dump(reposChanges, outfile)

    '''
    # load files changed during commit,
    # get the files by taking block comment above out
    # IT takes too much time to get the values with function above
    reposChanges = json.load(open('data.json'))

    #print(reposChanges)

    repo0 = reposChanges[repos[0]]
    repo1 = reposChanges[repos[1]]

    setDictList = []

    for repo in repos:
        setDict = {}
        for a in reposChanges[repo]:
            #for elem in a:
            for i in range(2, len(a)+1):
                if len(a) > 1 and len(a) < 15:
                    #print "len:", len(a)
                    #print "i:", i
                    combos = list(itertools.combinations(a, i))

                    for item in combos:
                        # print item

                        if item in setDict:
                            setDict[item] +=1

                            #if (setDict[item] > 2):
                                #if len(item) > 3:
                                    # print "item length:", len(item)
                                    # print "found set of:", setDict[item]
                        else:
                            setDict[item] = 0

        setDictList.append(setDict)

    twoSetsList     = []
    threeSetsList   = []
    fourSetsList    = []
    fiveSetsList    = []

    for ind, sets in enumerate(setDictList):
        print "\t" + repos[ind] + ":"
        for key, value in sets.iteritems():
            #print key
            if len(key) is 2 and value > 3 and len(twoSetsList) < 4:
                twoSetsList.append(key)

            if len(key) is 3 and value > 3 and len(threeSetsList) < 3:
                threeSetsList.append(key)

            if len(key) is 4 and value > 3 and len(fourSetsList) < 2:
                fourSetsList.append(key)

            if len(key) is 5 and value > 3 and len(fiveSetsList) < 1:
                fiveSetsList.append(key)

        print ""
        print "\t\ta) 4 sets of 2 files that changed together at least 3 times:"
        for index, items in enumerate(twoSetsList):
            print "\t\t\tSet:", index+1
            for i in items:
                print "\t\t\t\t-" + i
            print ""

        print "\t\tb) 3 sets of 3 files that changed together at least 3 times:"
        for index, items in enumerate(threeSetsList):
            print "\t\t\tSet:", index+1
            for i in items:
                print "\t\t\t\t-" + i
            print ""

        print "\t\tc) 2 sets of 4 files that changed together at least 3 times:"
        for index, items in enumerate(fourSetsList):
            print "\t\t\tSet:", index+1
            for i in items:
                print "\t\t\t\t-" + i
            print ""

        print "\t\td) 1 sets of 5 files that changed together at least 3 times:"
        for index, items in enumerate(fiveSetsList):
            print "\t\t\tSet:", index+1
            for i in items:
                print "\t\t\t\t-" + i
            print ""
        print ""

        #print combos
        # find the superset of elements


        # map and reduce elements
        # print elem

    '''
    counts = [0, 0, 0, 0, 0]         # will contain [0%-19.9%], [20%-39.9%], ...
    for keys, value in contributors[repos[0]].iteritems():
        dec = float(value[1])/float(a_ret) * 100
        if dec < 20.0:
            counts[0] += 1
        if dec >= 20.0 and dec < 40.0:
            counts[1] += 1
        if dec >= 40.0 and dec < 60.0:
            counts[2] += 1
        if dec >= 60.0 and dec < 80.0:
            counts[3] += 1
        if dec >= 80.0:
            counts[4] += 1

    #for keys in contributors[repos[0]]
    xObjects = ["0% to 20%", "20% to 40%", "40% to 60%", "60% to 80%", "80% to 100%"]
    y_pos = np.arange(len(xObjects))
    performance = counts

    plt.bar(y_pos, performance, align='center', alpha=1.0)
    plt.xticks(y_pos, xObjects)
    plt.ylabel('Number Of Users')
    plt.title('Number of Users Grouped By Commit Percentage')

    plt.show()
    '''

    # get hash value of commit
    # git log --pretty=format:"%h"

    # get files associated with commit hash
    # git diff-tree --no-commit-id --name-only -r <hash>
    # (ex. git diff-tree --no-commit-id --name-only -r 4e93138)



if __name__ == "__main__":
    main();
