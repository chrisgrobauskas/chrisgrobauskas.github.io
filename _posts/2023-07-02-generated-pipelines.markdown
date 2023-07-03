---
layout: post
title:  "Generated Pipelines"
date:   2023-07-02 20:00:00 -0500
categories: general
---
> "Each generation imagines itself to be more intelligent than the one that went before it, and wiser than the one that comes after it." ~ George Orwell

While this quote applies to the technology industry, I actually want to talk about code generation.

### Avoid Drudgery
One example of code generation is this blog.  It is hosted on [Github Pages](https://pages.github.com) and uses a tool called [Jekyll](https://jekyllrb.com) to render simple markdown documents as static webpages.  

Jekyll removes the need to write a large amount of boilerplate html and allows you to focus on writing.

This blog, though, is about generating Gitlab CI child pipelines.

### Companion Project
There is a companion [pipeline-welder project](https://gitlab.com/grobauskas/pipeline-welder) that has all the source code for this blog.  While it is a toy project, it is a working example for a Python + Jinja way to generate pipelines.  We will focus on generating Gitlab CI pipelines.

### Template Engines
All programming languages have code generation capabilities, but many languages also have tools that can render templates.  These tools can evaluate variables, functions, conditionals, loops, etc.

### Jinja Engine
[Jinja](https://jinja.palletsprojects.com/en/3.1.x/) is a Python template engine that has these capabilities and more.  The full Jinja template language is quite extensive, but we will only make use of conditional includes and variables.  

Hopefully by limiting ourselves it will make the concepts easier to follow.

Specifically, our Jinja template will:

- Generate a pipeline with build, test, and deploy stages
- The deploy stage will be optional and included only if the deploy job is requested
- The test stage will also have an optional lint job

You might note the ```rules``` command and variables in Gitlab CI would let you do the same things *without using a template library*.  

While this is contrived example to present the concept of generating and triggering a pipeline, there are cases where being able to do this can make your code simpler.  

### Jinja Template
What does a Jinja template look like?  

We will use the following template:

{% highlight jinja %}
{% raw %}
{# Sample pipeline in jinja format -- this is a comment #}
stages:
  - build
  - test
{% if deploy %}
  - deploy
{% endif %}

build-job:
  stage: build
  script:
    - echo "{{ build_command }}"

unit-test-job:
  stage: test
  script:
    - echo "{{ test_command }}"

{% if lint %}
lint-test-job:
  stage: test
  script:
    - echo "Linting ..."
{% endif %}

{% if deploy %}
deploy-job:
  stage: deploy
  environment: {{ environment_name }}
  script:
    - echo "Deploying application..."
{% endif %}
{% endraw %}
{% endhighlight %}

#### Default Behavior
In general, Jinja will simply output the inline text.  Jinja also has has a tagging syntax using ```{% raw %}{{ }}{% endraw %}``` braces.  

Tags are how we will tell Jinja what actions to take to modify output while rendering our template.

Jinja evaluates the text between the braces to allow comments, conditional execution, variable replacement, loops, etc.  We will only look at the first three.  

> For a full listing of features see the [Jinja](https://jinja.palletsprojects.com/en/3.1.x/) website!

This section shows a comment:

{% highlight jinja %}
{% raw %}
{# Sample pipeline in jinja format -- this is a comment #}
{% endraw %}
{% endhighlight %}

This is an example of an if block that will include the nested line if the expression is true.

{% highlight jinja %}
{% raw %}
{% if deploy %}
  - deploy
{% endif %}
{% endraw %}
{% endhighlight %}

Finally, this is an example of variable replacement.  The space between the braces will be replaced with the value of ```build_command```.  Note, the braces are also replaced as they are just tags for Jinja to find, evaluate, and replace.

{% highlight jinja %}
{% raw %}
    - echo "{{ build_command }}"
{% endraw %}
{% endhighlight %}

### Project Structure
Our companion [pipeline-welder project](https://gitlab.com/grobauskas/pipeline-welder) has the following directory structure:

```
.
├── templates
│   └── jinja_sample.txt
├── welder
│   └── tests
│   |   └── welder_test.py
│   ├── LICENSE.txt
│   ├── README.md
│   ├── __init__.py
│   ├── __main__.py
│   ├── pyproject.toml
│   ├── requirements.txt
│   ├── README.md
│   └── welder.py
├── .gitignore
├── .gitlab-ci.yml
├── LICENSE.txt
├── README.md

```

Feel free to use the code as you see fit.  It is licensed under the MIT license.  Just keep in mind this is a toy project and would need more work for a production setting.

### Project Flowchart
As a part of running the ```.gitlab-ci.yml``` pipeline, Gitlab will start two jobs ```plan``` and ```apply```.

First, the plan job will run the welder.py program which will receive command line inputs.  We will request the optional deploy job be included.  However, we will not request linting; so this optional job will not run.  Additionally, we will provide commands to run during the build and test jobs of the generated pipeline as well as the environment name for the deploy job.

The Jinja Engine will combine the template with the inputs when we call the ```render()``` function.  After rendering, we will write the generated pipeline output to a file.

Second, the apply job will use the trigger command to submit the generated pipeline to run independently as a child pipeline.

![flow](/assets/generated-pipelines/drawio-parent-child.png){:class="img-responsive"}

### Gitlab Screens
This is what you see within Gitlab for the project's ```.gitlab-ci.yml``` when it runs.

![plan-apply](/assets/generated-pipelines/plan-apply.png){:class="img-responsive"}

Only the plan and apply jobs are part of the parent pipeline.  The apply job itself creates the *Downstream* pipeline by issuing a ```trigger``` command.  You can click through the Downstream pipeline to see the generated, child pipeline.

![plan-apply-child](/assets/generated-pipelines/plan-apply-child.png){:class="img-responsive"}

### Parent Pipeline
What does the parent ```.gitlab-ci.yml``` code look like?

{% highlight yaml %}
stages:
    - plan
    - apply

plan:
  stage: plan
  image: python:latest
  script: 
    - python -m venv venv
    - . venv/bin/activate
    - pip install -r welder/requirements.txt
    - python welder/welder.py 
      -t templates/jinja_sample.txt 
      -o generated_job.yml 
      -k build_command="Can we build it?" 
      test_command="Yes we can!" 
      environment_name=unit 
      lint=False 
      deploy=True  
      -v
    - pwd;ls -l

  artifacts: 
    paths: 
      - ./generated_job.yml

apply:
  stage: apply
  trigger:
    include:
      - artifact: generated_job.yml
        job: plan
    strategy: depend
{% endhighlight %}

> The use of ```image: python:latest``` on gitlab.com is ok for a toy project.  It would be better for a production environment to build your own image where you can control the versions of software in the image.

First, the **plan job** sets up a python virtual environment and installs dependencies.  Next, the ```welder.py``` program runs and receives several arguments:

  - ```-t``` 
      - This is the Jinja template file
  - ```-o``` 
      - This is the output file 
  - ```-k``` 
      - This is a list of key=value options
        - The following inputs are passed as key=value pairs for replacement:
          - build_command="Can we build it?"
          - test_command="Yes we can!"
          - environment_name=unit
        - The following inputs are passed as key=value pairs for controlling which jobs to include:
          - lint=False 
          - deploy=True  
  - ```-v``` 
      - This is a verbose option

After the python program exits, the ```artifacts``` command is used to save the output from the python script as an artifact named ```./generated_job.yml```.

Finally, the **apply job** uses the ```trigger``` command to submit a child pipeline with the artifact named ```./generated_job.yml```.  It uses a ```strategy: depend``` to tell the the parent pipeline to wait for the child pipeline to complete.

So, while the child pipeline runs independently of the parent, the parent will wait for completion of the child before exiting.

#### Plan Job
If we peek inside the plan job in the parent pipeline, we can see what the job run looked like including the ```generated_pipeline.yml``` artifact being saved.

![plan-apply](/assets/generated-pipelines/plan-apply.png){:class="img-responsive"}

![plan-job](/assets/generated-pipelines/plan-job.png){:class="img-responsive"}

#### Artifacts
Artifacts are outputs from jobs that Gitlab will save and optionally pass to other commands.

To view the ```generated_job.yml``` artifact, on the right hand side of the job window we can choose an option under Job Artifacts: "Download" to download a zip file of all artifacts or "Browse" to see a list of artifacts.  We will choose "Browse".

![job-artifacts](/assets/generated-pipelines/job-artifacts.png){:class="img-responsive"}

From the "Browse" screen we can click on the artifact and choose to download the ```generated_job.yml``` file to our workstation.

![browse-artifacts](/assets/generated-pipelines/browse-artifacts.png){:class="img-responsive"}

Below are the contents of the downloaded ```generated_job.yml``` file.  We can see that variable replacement and conditional includes have been evaluated based on the inputs for ```welder.py``` above.

{% highlight yaml %}
stages:
  - build
  - test
  - deploy

build-job:
  stage: build
  script:
    - echo "Can we build it?"

unit-test-job:
  stage: test
  script:
    - echo "Yes we can!"


deploy-job:
  stage: deploy
  environment: unit
  script:
    - echo "Deploying application..."

{% endhighlight %}

### Python welder.py
The ```welder.py``` program is what is calling Jinja. 

- First, ```main()``` is called to handle command line arguments  
- Second, ```gitlab_jinja()``` is called to set up Jinja and call ```render()```   
- Finally, output is written to a stdout or a file 

Here is the code in its entirety.  If you prefer you can view the code in the gitlab project [here](https://gitlab.com/grobauskas/pipeline-welder).

{% highlight Python %}
import argparse
import errno
from jinja2 import Environment, FileSystemLoader
from os.path import basename, dirname, exists, isfile, realpath
import os
import sys


def gitlab_jinja(template_file=None, output_file=None, verbose=None, **welder_kv):
    """gitlab jinja planner for welder pipeline assembler

    Keyword arguments:
    template_file -- the path to the template file to evaluate
    output_file -- the generated gitlab pipeline
    verbose -- verbose switch
    welder_kv -- key-value for evaluation/replacement
    """
    if not exists(template_file):
        print(f"ERROR: template_file '{template_file}' does not exist!")
        sys.exit(1)
    elif not isfile(template_file):
        print(f"ERROR: template_file '{template_file}' is a directory!")
        sys.exit(1)

    template_file_dir = dirname(realpath(template_file))
    template_file_basename = basename(template_file)

    environment = Environment(
        loader=FileSystemLoader(template_file_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template_file = environment.get_template(template_file_basename)

    content = template_file.render(**welder_kv)

    if output_file == "stdout":
        sys.stdout.write(content)
    else:
        with open(output_file, mode="w", encoding="utf-8") as pipeline:
            pipeline.write(content)

    if verbose == True:
        print(f"INFO: Created {output_file}")


def main():
    """CLI for welder dynamic gitlab pipelines"""
    parser = argparse.ArgumentParser(
        prog="welder", description="assemble dynamic gitlab pipelines"
    )

    parser.add_argument("-o", "--output_file", action="store", default="stdout")
    parser.add_argument("-t", "--template-file", action="store", required="true")
    parser.add_argument("-v", "--verbose", action="store_true")
    parser.add_argument(
        "-k",
        "--keywords",
        nargs="+",
        action="append",
        help="keyword pairs with quotes for whitespace",
    )

    args = parser.parse_args()

    if not exists(args.template_file):
        print(f"ERROR: template '{args.template_file}' does not exist!")
        sys.exit(1)

    if exists(args.output_file) and args.output_file != "stdout":
        print(f"WARNING: output_file file '{args.output_file}' will be overlaid!")

    welder_kv = {}
    for key_pair_list in args.keywords:
        for key_pair in key_pair_list:
            key_list = key_pair.split("=")
            if len(key_list) > 1:
                if key_list[1].upper() == "FALSE":
                    welder_kv.update({key_list[0]: False})
                elif key_list[1].upper() == "TRUE":
                    welder_kv.update({key_list[0]: True})
                elif isinstance(key_list[1], int):
                    welder_kv.update({key_list[0]: int(key_list[1])})
                elif isinstance(key_list[1], float):
                    welder_kv.update({key_list[0]: float(key_list[1])})
                else:
                    welder_kv.update({key_list[0]: key_list[1]})
            else:
                welder_kv.update({key_list[0]: True})

    if args.verbose:
        print(
            f"""
            Welder Input:
            template-file={args.template_file}
            output_file={args.output_file}
            verbose={args.verbose}
            keywords={args.keywords}
            welder_kv={welder_kv}
            """
        )

    gitlab_jinja(args.template_file, args.output_file, args.verbose, **welder_kv)


if __name__ == "__main__":
    main()
{% endhighlight %}

### Lines of Code
As you can see from scanning the code above, most of the code in this  program is for handling command line options in ```main()```.

The second largest amount of code is for file I/O in ```gitlab_jinja()``` where we validate the template exists, format the path for the template directory, and later write the rendered template to stdout or a file.

I also noted while writing the blog that I have duplicate file existence checks in ```main()``` and ```gitlab_jinja()```.  While they do need to be checked in both places in case the function is called outside the main(), the checks could be refactored into a function.

#### Crazy Eights
Only the following 8 lines of code in ```gitlab_jinja()``` are directly related to rendering templates.

{% highlight Python %}
    environment = Environment(
        loader=FileSystemLoader(template_file_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template_file = environment.get_template(template_file_basename)

    content = template_file.render(**welder_kv)
{% endhighlight %}

- First, the ```Environment()``` function loads the template directory as a source and tells Jinja what we want to do with whitespace
- Second, the ```get_template()``` function does exactly what it sounds like it does
- Finally, the ```render()``` function receives a key value dictionary within inputs from the command line and transforms the template into content

So, the code required to render a template is very small.

### Future Research
I hope I have made you more interested in Jinja and generated child pipelines in Gitlab.  When used appropriately both can simplify workflows.

We barely touched on Jinja's extensive feature set, and you also get all the other things Python can do when you're using Jinja.

So, you're only limited to what you can buy, borrow, or steal (legally reuse open source code).  Happy coding!
