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


def renderTemplateFromString(templates_dir, template_string, context):
    return jinja2.Environment(
        loader=jinja2.FileSystemLoader(templates_dir or './')
    ).from_string(template_string).render(context)


if __name__ == "__main__":
    env_template_config = os.environ.get(
        "TEMPLATE_CONFIG_FILE", "./templating.yaml")
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

    # Work out which templates we are calculating
    if templates == "all":
        work = config["packages"]
    else:
        work = {}
        for t in templates:
            work[t] = config["packages"][t]

    for exporter_name, exporter_config in work.items():
        logging.info("Building exporter {}".format(exporter_name))

        # First we need to work out the context for this build
        context = exporter_config["context"]["static"]

        # Add in the exporter name as a context variable
        context["name"] = exporter_name

        # Use the compiled contexts to build the dynamic contexts.
        # Dynamic contexts can use other dynamic contexts as long
        # as they are compiled before.
        to_process = exporter_config["context"]["dynamic"]
        for context_name, to_template in to_process.items():
            print(context_name)
            if type(to_template) is str:
                context[context_name] = renderTemplateFromString(
                    templates_dir=templates_dir,
                    template_string=to_template,
                    context=context
                )
            elif type(to_template) is list:
                context_element = []
                for item in to_template:
                    context_element.append(renderTemplateFromString(
                        templates_dir=templates_dir,
                        template_string=item,
                        context=context)
                    )
                context[context_name] = context_element
            else:
                raise TypeError("Invalid type {} for key {}".format(
                    type(to_template), context_name))

        print(context)

        for build_step, template in exporter_config['build_steps'].items():
            output = "{name}/autogen_{name}.{build_step}".format(**{
                'name': exporter_name,
                'build_step': build_step,
            })

            logging.info("Rendering step {} for {}".format(
                build_step, exporter_name))
            rendered = renderTemplateFromString(templates_dir=templates_dir,
                                                template_string=template,
                                                context=context)
            logging.info("Writing {} step {} to {}".format(
                exporter_name, build_step, output))
            # print(rendered)
            with open(output, 'w') as output_file:
                output_file.write(rendered)
