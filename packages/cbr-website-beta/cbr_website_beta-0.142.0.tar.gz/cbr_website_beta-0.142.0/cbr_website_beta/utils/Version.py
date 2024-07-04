import cbr_website_beta
from osbot_utils.base_classes.Type_Safe import Type_Safe
from osbot_utils.utils.Files            import file_contents, path_combine

class Version(Type_Safe):

    FILE_NAME_VERSION = 'version'

    def path_code_root(self):
        return cbr_website_beta.path

    def path_version_file(self):
        return path_combine(self.path_code_root(), self.FILE_NAME_VERSION)

    def value(self):
        value = file_contents(self.path_version_file()) or ""
        return value.strip()

version = Version().value()     # todo: replace use of this method with the version__cbr_website

version__cbr_website = Version().value()