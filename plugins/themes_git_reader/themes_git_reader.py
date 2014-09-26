import os, sys
import logging
from glob import glob
from pelican import signals
#from pelican.readers import MarkdownReader, RstReader, Readers

logger = logging.getLogger(__name__)
try:
    from sh import git
except ImportError as ie:
    logger.error("Import Error: {0}".format(ie))
    sys.exit(1)


########
# priv #
########
def find_images(Folder, FileEndings):
    Images = []
    for FileEnding in FileEndings:
        Images = glob(os.path.join(Folder, FileEnding)) + Images
    return Images

def find_title(File): #stub
    return File

def generate_json_url(Settings, Folder):
    return "{0}/{1}/{2}.json".format(
                        Settings['SITEURL'],
                        Settings['JSON_OUT'],
                        Folder)
    

def crawl_themes(Settings):
    Themes = []
    for Folder in os.listdir(Settings['GIT_DIR']):
        CurrentDir = os.path.join(Settings['GIT_DIR'], Folder)
        if os.path.isdir(CurrentDir):
            Theme = {}
            Theme['images'] = find_images(CurrentDir, Settings['IMAGE_FILE_ENDINGS'])
            Theme['title'] = find_title(Folder)
            Theme['json_url'] = generate_json_url(Settings, Folder)
            #todo extract more info from readme's, use pelicans readers?
            Themes = [Theme] + Themes
    return Themes

########
# pub  #
########
def pelican_initialized(pelican):
    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('GIT_URL',
        'https://github.com/getpelican/pelican-themes.git')
    DEFAULT_CONFIG.setdefault('GIT_DIR', 'git_input')
    DEFAULT_CONFIG.setdefault('IMAGE_FILE_ENDINGS',
        ['*.png', '*.PNG', '*.jpg', '*.JPG'])
    DEFAULT_CONFIG.setdefault('JSON_OUT', 'json')
    if pelican:
        pelican.settings.setdefault('GIT_URL',
            'https://github.com/getpelican/pelican-themes.git')
        pelican.settings.setdefault('GIT_DIR', 'git_input')
        pelican.settings.setdefault('README_FILE_NAMES',
            ['readme.md', 'README.md', 'readme.rst', 'README.rst'])
        pelican.settings.setdefault('IMAGE_FILE_ENDINGS',
            ['*.png', '*.PNG', '*.jpg', '*.JPG'])
        pelican.settings.setdefault('JSON_OUT', 'json')

def initialize(article_generator):
    logger.debug('start initializing themes_git_reader')
    StartingDir = os.getcwd()
    RepoDir = article_generator.settings['GIT_DIR']
    if os.path.exists(RepoDir):
        logger.debug('updating repository at %s' % RepoDir)
        os.chdir(RepoDir)
        git.pull()
    else:
        logger.debug('cloning repository to %s' % RepoDir)
        git.clone(article_generator.settings['GIT_URL'], article_generator.settings['GIT_DIR'])
        os.chdir(RepoDir)
    logger.debug('update submodules in %s' % RepoDir)
    git.submodule.update("--init", "--recursive")
    os.chdir(StartingDir)
    logger.debug('finished initializing themes_git_reader')

def generate_articles(context):
    logger.debug('writing articles from gitrepo')
    themes = crawl_themes(context.settings)
    for theme in themes:
        print(repr(theme))
        input()


def register():
    signals.initialized.connect(pelican_initialized)
    signals.article_generator_init.connect(initialize)
    signals.article_generator_finalized.connect(generate_articles)