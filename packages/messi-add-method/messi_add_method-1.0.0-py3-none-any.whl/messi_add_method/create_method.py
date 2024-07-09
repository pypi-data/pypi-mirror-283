import logging
import yaml
import os
import sys
import jinja2
import shutil
from pathlib import Path
from docopt import docopt


log = logging.getLogger(__name__)

class MethodCreate:
  """Creates relevant nextflow modules or subworkflows and their corresponding
  scripts that a method should inherit and have from template

  Args:
    name (str): Name of the method
    language (str): Language that the method was implemented in
    outdir (str): Path to local output directory
    template_yaml_path (str): Path to template.yml for the method creation settings
  """

  def __init__(
      self,
      name,
      language,
      outdir=None,
      template_yaml_path=None
  ):
    
    # Load temperate params and yml
    self.template_params, self.template_yml = self.create_params_dict(
      name, language, template_yaml_path, outdir if outdir else "."
    )

    # Setting convenient vars
    self.name = self.template_params["name"]
    self.language = self.template_params["language"]
    self.outdir = Path(outdir)
  
  def create_params_dict(self, name, language, template_yaml_path, outdir):
    """Creates dictionary of parameters from config yml

    Args:
      name (str) : Name for the method
      language (str): Language that the method was implemented in
      template_yaml_path (str): Path to YAML file containing template parameters
    """

    # Obtain info from yaml
    try:
      if template_yaml_path is not None:
        with open(template_yaml_path) as f:
          template_yaml = yaml.safe_load(f)
      else:
        template_yaml = {}
    except FileNotFoundError:
      raise UserWarning(f"Template YAML file '{template_yaml_path}' not found.")

    # Also create a new dict to store necessary info
    param_dict = {}
    param_dict["name"] = self.get_param("name", name, template_yaml, template_yaml_path)
    param_dict["language"] = self.get_param("language", language, template_yaml, template_yaml_path)

    return param_dict, template_yaml
  
  # TODO: need to implement to use a better way asking user input
  def get_param(self, param_name, passed_value, template_yaml, template_yaml_path):
    if param_name in template_yaml:
        if passed_value is not None:
            log.info(f"overriding --{param_name} with name found in {template_yaml_path}")
        passed_value = template_yaml[param_name]
    return passed_value

  def init_method(self):
      """
      Creates the method relevant files
      """
      # Create files from templates using jinja
      self.render_template()
      return None
  def render_template(self):
    """Runs jinja to create all relevant files for the method"""
    log.info(f"Creating relevant files for: '{self.name}'")

    # current_dir = os.path.dirname(os.path.abspath(__file__))

    # # Navigate to the parent directory (root)
    # root_dir = os.path.dirname(current_dir)
    # template_dir = os.path.join(root_dir, "method-template")
    # Run jinja2 for each file in the template folder

    env = jinja2.Environment(
      loader=jinja2.PackageLoader('messi_add_method', 'method-template'),
      keep_trailing_newline=True
    )

    # TODO: need to better handle this path using os
    object_attrs = self.template_params
    name = object_attrs["name"]
    try:
      if object_attrs["language"].lower() == 'r':
        ext = "R"
      elif object_attrs["language"].lower() == 'python':
        ext = "py"
      object_attrs["ext"] = ext
    except Exception:
      raise NotImplementedError
    
    template_dir = os.path.join(os.path.dirname(__file__), "method-template")
    # Then glob the template files
    # POSIX might not work on windows
    template_files = list(Path(template_dir).glob("**/*"))
    template_files += list(Path(template_dir).glob("*"))
    # files to ignore
    ignore_strs = [".pyc", "__pycache__", ".pyo", ".pyd", ".DS_Store", ".egg", ".yaml"]
    # Then rename some templates to the one using method name
    resource_prefix = "resources/usr/bin"
    # TODO: this is very ugly now .....
    rename_files = {
      # The main workflow of the method
      "subworkflows/methods/method/main.nf": f"subworkflows/methods/{name}/main.nf",
      # And for each action in preprocess, train, predict, select_feature, and their resource script
      # PREPROCESS
      "modules/method/preprocess/main.nf" :     f"modules/{name}/preprocess/main.nf",
      "modules/method/train/main.nf" :          f"modules/{name}/train/main.nf",
      "modules/method/predict/main.nf" :        f"modules/{name}/predict/main.nf",
      "modules/method/select_feature/main.nf" : f"modules/{name}/select_feature/main.nf",
      # And the resources scripts
      #f"modules/method/preprocess/{resource_prefix}/method_preprocess.{ext}":  f"modules/{name}/preprocess/{resource_prefix}/{name}_preprocess.{ext}",
      #f"modules/method/train/{resource_prefix}/method_train.{ext}":  f"modules/{name}/train/{resource_prefix}/{name}_train.{ext}",
      #f"modules/method/predict/{resource_prefix}/method_predict.{ext}":  f"modules/{name}/predict/{resource_prefix}/{name}_predict.{ext}",
      #f"modules/method/select_feature/{resource_prefix}/method_select_feature.{ext}":  f"modules/{name}/select_feature/{resource_prefix}/{name}_select_feature.{ext}"
    }
    
    # Then loop through all template files
    for template_fn_path_obj in template_files:
        template_fn_path = str(template_fn_path_obj)
        if os.path.isdir(template_fn_path):
          continue
        if any([s in template_fn_path for s in ignore_strs]):
          log.debug(f"Ignoring '{template_fn_path}' in jinja2 template creation")
          continue
        # Set up vars and directories
        template_fn = os.path.relpath(template_fn_path, template_dir)
        output_path = self.outdir / template_fn
  
        if template_fn in rename_files:
            output_path = self.outdir / rename_files[template_fn]
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
        # Then rest should just do this:
        try:
          log.debug(f"Rendering template file: '{template_fn}'")
          j_template = env.get_template(template_fn)
          rendered_output = j_template.render(object_attrs)
          # Mirror file permissions
          # Write to the output file
          with open(output_path, "w") as fh:
            log.debug(f"Writing to output file: '{output_path}'")
            fh.write(rendered_output)
        # Copy the file directly instead of using Jinja
        #except (AttributeError, UnicodeDecodeError) as e:
          #log.debug(f"Copying file without Jinja: '{output_path}' - {e}")
          #shutil.copy(template_fn_path, output_path)
        # Something else went wrong
        except Exception as e:
          print(f"Template could not be copied: '{template_fn_path}'")
          #log.error(f"Copying raw file as error rendering with Jinja: '{output_path}' - {e}")
          #shutil.copy(template_fn_path, output_path)
        template_stat = os.stat(template_fn_path)
        os.chmod(output_path, template_stat.st_mode)
    # DONE the for loop
    return None
