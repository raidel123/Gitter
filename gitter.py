import os
import subprocess

repos = ["commons-math", "pdfbox"]
repoInfo = {}

def main():

    wd = os.getcwd()
    for repo in repos:

        repoInfo[repo] = []

        os.chdir(repo)

        '''
        for l in range(ord('a'), ord('i')+1):
            print chr(l)
        '''

        # 1.a : overall number of commits, per repo
        a = subprocess.check_output('git rev-list --count HEAD')
        a = a.rstrip('\n')
        #remove newlines, add result to dict
        repoInfo[repo].append(('a', a))


        # 1.b : average number of commits per file, per repo
        filesInRepos = subprocess.Popen(('git ls-files'), stdout=subprocess.PIPE)
        fileCount = subprocess.check_output(('wc -l'), stdin=filesInRepos.stdout)
        filesInRepos.wait()     # wait for subprocess to finish

        #print fileCount
        b = float(a) / float(fileCount.rstrip('\n'))
        repoInfo[repo].append(('b', b))

        # 1.c : number of contributors, per repos


        # 1.d : average number of commits per contributor, per repo


        # 1.e : percentage of changes done by each contributor, per repo


        # 1.f : people that contributed to both projects, number of commits to each repo


        # 1.g : which contributors have been inactive for past six months or more, per repo


        # 1.h : number of files added, deleted, modified in the past year, per repo


        # 1.i : summarize what was observed. Similarities, differences

        # cd back to calling directory

        # print answer lists for each repo
        print repo + ":", repoInfo[repo]

        os.chdir(wd)

        '''
        os.chdir(dir)
        print os.listdir('.')
        os.chdir("..")
        print ""
        '''

if __name__ == "__main__":
    main();
