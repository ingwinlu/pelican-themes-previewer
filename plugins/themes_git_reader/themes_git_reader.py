import os, sys
import logging
import string
from glob import glob
from pelican import signals
from pelican.contents import Article, Static
from pelican.urlwrappers import Category
from pelican.utils import get_date
#from pelican.readers import MarkdownReader, RstReader, Readers

logger = logging.getLogger(__name__)
Themes = []
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

def get_last_modified(GitFolder, Folder):
    StartingDir = os.getcwd()
    os.chdir(GitFolder)
    Date = str(git.log("-n1", "--format='%ai'", "--", Folder))
    Date = Date.split("'")[1]
    Date = get_date(Date)
    os.chdir(StartingDir)
    return Date

def get_category(Settings):
    #could be extended to check if theme got updated, or is new theme
    return Category("theme", Settings)
    
def generate_json_url(Settings, Folder):
    return "{0}/{1}/{2}.json".format(
                        Settings['SITEURL'],
                        Settings['JSON_OUT'],
                        Folder)
    

def crawl_themes(Settings):
    Themes = []
    for Folder in os.listdir(Settings['GIT_DIR']):
        PrefixedDir = os.path.join(Settings['GIT_DIR'], Folder)
        if os.path.isdir(PrefixedDir) and not Folder in Settings['EXCLUDE_GIT_DIRS']:
            Theme = {}
            Theme['images'] = find_images(PrefixedDir, Settings['IMAGE_FILE_ENDINGS'])
            Theme['title'] = find_title(Folder)
            Theme['date'] = get_last_modified(Settings['GIT_DIR'], Folder)
            Theme['category'] = get_category(Settings)
            Theme['json_url'] = generate_json_url(Settings, Theme['title'])
            #todo extract more info from readme's, use pelicans readers?
            Themes = [Theme] + Themes
    return Themes

def init_git(Pelican):
    logger.debug('start initializing git')
    StartingDir = os.getcwd()
    RepoDir = Pelican.settings['GIT_DIR']
    if os.path.exists(RepoDir):
        logger.debug('updating repository at %s' % RepoDir)
        os.chdir(RepoDir)
        git.pull()
    else:
        logger.debug('cloning repository to %s' % RepoDir)
        git.clone(Pelican.settings['GIT_URL'], Pelican.settings['GIT_DIR'])
        os.chdir(RepoDir)
    logger.debug('update submodules in %s' % RepoDir)
    git.submodule.update("--init", "--recursive")
    os.chdir(StartingDir)
    logger.debug('finished initializing git')

########
# pub  #
########
def initialize(Pelican):
    from pelican.settings import DEFAULT_CONFIG
    DEFAULT_CONFIG.setdefault('GIT_URL',
        'https://github.com/getpelican/pelican-themes.git')
    DEFAULT_CONFIG.setdefault('GIT_DIR', 'git_input')
    DEFAULT_CONFIG.setdefault('IMAGE_FILE_ENDINGS',
        ['*.png', '*.PNG', '*.jpg', '*.JPG'])
    DEFAULT_CONFIG.setdefault('JSON_OUT', 'json')
    DEFAULT_CONFIG.setdefault('EXCLUDE_GIT_DIRS', ['.git', 'pelicanthemes-generator'])
    if Pelican:
        Pelican.settings.setdefault('GIT_URL',
            'https://github.com/getpelican/pelican-themes.git')
        Pelican.settings.setdefault('GIT_DIR', 'git_input')
        Pelican.settings.setdefault('README_FILE_NAMES',
            ['readme.md', 'README.md', 'readme.rst', 'README.rst'])
        Pelican.settings.setdefault('IMAGE_FILE_ENDINGS',
            ['*.png', '*.PNG', '*.jpg', '*.JPG'])
        Pelican.settings.setdefault('JSON_OUT', 'json')
        Pelican.settings.setdefault('EXCLUDE_GIT_DIRS', ['.git', 'pelicanthemes-generator'])
        init_git(Pelican)
        global Themes
        Themes = crawl_themes(Pelican.settings)

def add_articles_to_article_list(article_generator):
    logger.debug('add_articles_to_article_list')
    global Themes
    Articles = []
    for Theme in Themes:
        Articles = [
                Article(
                    content='',
                    metadata=Theme,
                    settings=article_generator.settings)
            ] + Articles
    article_generator.articles = Articles

def add_static_to_static_list(static_generator):
    logger.debug('add_static_to_static_list')
    pass

def register():
    signals.initialized.connect(initialize)
    signals.article_generator_pretaxonomy.connect(add_articles_to_article_list)
    signals.static_generator_init.connect(add_static_to_static_list)