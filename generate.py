#!/usr/bin/python3

'''
This script generates spec, unit and init files for CentOS build_filess.
'''

import jinja2
import yaml
import os
import logging
import argparse

def renderTemplateFromFile(templates_dir, template_file, context):
	return jinja2.Environment(
			loader=jinja2.FileSystemLoader(templates_dir or './')
		).get_template(template_file).render(context)

def renderTemplateFromString(template_string, context):
	return jinja2.Environment(
		loader=jinja2.BaseLoader
	).from_string(template_string).render(context)

if __name__ == "__main__":
	env_template_config = os.environ.get("TEMPLATE_CONFIG_FILE", "./templating.yaml")
	env_templates_dir = os.environ.get("TEMPLATES_DIRECTORY", "./templates/")
	
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('--templates', metavar='N', type=str, nargs='+',
					default='all',
                    help='A list of templates to generate')
	parser.add_argument('--template-config', metavar='file', type=str,
					default=env_template_config,
                    help='The configuration file to generate templates with')
	parser.add_argument('--templates-dir', metavar='directory', type=str,
					default=env_templates_dir,
                    help='The directory that templates are stored in')

	args = parser.parse_args()

	templates = args.templates
	template_config = args.template_config
	templates_dir = args.templates_dir


	logging.basicConfig(level=logging.INFO)


	with open(template_config, 'r') as tc:
		config = yaml.load(tc)

	defaults = config["defaults"]

	# Work out which templates we are calculating
	if templates == "all":
		work = config["packages"]
	else:
		work = {}
		for t in templates:
			work[t] = config["packages"][t]

	for exporter_name, exporter_config in work.items():
		logging.info("Building exporter {}".format(exporter_name))

		# Build the configuration as a merge of the defaults and the exporter config
		context = {
			"name": exporter_name,
			"license": exporter_config["license"],
			"description": exporter_config["description"],
			"summary": exporter_config["summary"],
			"version": exporter_config["version"],
			"URL": exporter_config["URL"],
			"package": exporter_config.get("package", defaults["package"]),
			"build_steps": exporter_config.get("build_steps", defaults["build_steps"]),
			"user": exporter_config.get("user", defaults["user"]),
			"group": exporter_config.get("group", defaults["group"]),

			# These are all run through a jinja2 template with the above context
			"tarball_unformatted": exporter_config.get("tarball", defaults["tarball"]),
			"sources_unformatted": exporter_config.get("sources", defaults["sources"]),
			"sources": [],
			"prep_unformatted": exporter_config.get("prep", defaults["prep"]),
			"build_unformatted": exporter_config.get("build", defaults["build"]),
			"install_unformatted": exporter_config.get("install", defaults["install"]),
			"pre_unformatted": exporter_config.get("pre", defaults["pre"]),
			"post_unformatted": exporter_config.get("post", defaults["post"]),
			"preun_unformatted": exporter_config.get("preun", defaults["preun"]),
			"postun_unformatted": exporter_config.get("postun", defaults["postun"]),
			"files_unformatted": exporter_config.get("files", defaults["files"]),
		}

		# Run the templating over these sections with the above context
		context["tarball"] = renderTemplateFromString(context["tarball_unformatted"], context)
		context["prep"] = renderTemplateFromString(context["prep_unformatted"], context)
		context["build"] = renderTemplateFromString(context["build_unformatted"], context)
		context["install"] = renderTemplateFromString(context["install_unformatted"], context)
		context["pre"] = renderTemplateFromString(context["pre_unformatted"], context)
		context["post"] = renderTemplateFromString(context["post_unformatted"], context)
		context["preun"] = renderTemplateFromString(context["preun_unformatted"], context)
		context["postun"] = renderTemplateFromString(context["postun_unformatted"], context)
		context["files"] = renderTemplateFromString(context["files_unformatted"], context)

		context['sources'] = []
		for source_template in context['sources_unformatted']:
			context['sources'].append(renderTemplateFromString(source_template, context))

		logging.debug("Using context {}".format(context))

		for build_step in context['build_steps']:
			template_file = "{}.tpl".format(build_step)
			output = "{name}/autogen_{name}.{build_step}".format(**{
				'name': context['name'],
				'build_step': build_step,
			})
			logging.info("Rendering template {}/{}".format(templates_dir, template_file))
			rendered = renderTemplateFromFile(templates_dir=templates_dir, template_file=template_file, context=context)
			logging.info("Writing {} step {} to {}".format(exporter_name, build_step, output))
			with open(output, 'w') as output_file:
				output_file.write(rendered)


