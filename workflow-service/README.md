#### Lambda Python Package Builder guide
This is the guide to create and package Python library/package dependencies to be used inside of AWS Lambda functions for the NaaVRE [examples on Github](https://github.com/QCDIS/tmp-devops-test-workflows).

> Please, notice that for this particular case, we're installing the libraries as specicified on [NaaVRE Github Example Page](https://github.com/QCDIS/tmp-devops-test-workflows) for the `use-case-icos`. All commands are manually set. In case you have different dependencies and configurations (e.g., Python runtime), please change that in the code.

> You may remove the first line from each code snippet. This is assuming that you're going to store this in `.sh` files and run them. Note: for that, after you create them, you must run `chmod +x your_shell_command.sh` in order for it to be executable by your system.
1. Installation of Python packages locally using `venv`
```sh
#!/bin/bash
python3 -m venv naavre_env
source naavre_env/bin/activate || exit
```

2. Running `pip` install inside of the `venv`. This creates a zipped folder `python` that you should upload to either S3 (and use its link inside of AWS Lambda Layers) or directly into a Layer object. _Please notice that AWS sets a limit for the Layer's package size, so keep that in mind depending on the service that you want to use._
```sh
#!/bin/bash
pip install --platform manylinux2014_x86_64 --target=python --implementation cp --python-version 3.11 --only-binary=:all: --upgrade icoscp==0.2.2 icoscp_core==0.3.9 matplotlib python-slugify || exit
zip -r python.zip python || rm -rf python
```

3. Upload the code into AWS Lambda through the Console or AWS CLI.

4. Fixing errors inside the code.
> This sort of errors are more open-ended and might question the feasibility of the project. If those patterns are the same for every package, then the coverage is ensured. However, we're not sure about this. If you have any time error, probably is related with the specificity of the library/package you're using.
- Had to create a temporary folder path for some libraries to work
```py
import os
os.environ['HOME'] = '/tmp'
```
- Defining a `/tmp/data` folder to satisfy a write command inside of the function
> Ref (second comment    ): https://stackoverflow.com/questions/31938828/aws-lambda-downloading-a-file-and-using-it-in-the-same-function-nodejs
```py
# Ensure the /tmp/data directory exists
data_dir = '/tmp/data'
os.makedirs(data_dir, exist_ok=True)
```

---

#### Notes
- Uploaded to S3 because of the limit in Layers, which is roughly ~50MB.
- Runtime 3.11 because of the Numpy dependencies for compilation. This was noted because while compiling there were several incompatibility errors thrown, specifically by `numpy` package. After some trial and error, we figured out that we had to run this on the `3.11` version of Python.

- ⁠Imported all the cells into one (copy/paste) just for fast validation
- ⁠⁠Solved runtime issues and binary targeting for the libraries—I am assuming that’s what you were having problems with
- ⁠⁠Fixed some syntax errors (inside of the code actually)
     - `if isinstance(d, str) and (d == 'no data available'):` was changed to `if isinstance(datasets, str) and (datasets == 'no data available'):`
- ⁠⁠Fixed temporary folder for cache stuff—I’ll explain this later
- Create an account to get the token: https://cpauth.icos-cp.eu/home/
- Changed the timeout from Lambda from the default `3s` to `>3m`. In this case, timeout is of no use.

#### To-dos
- [ ] Verify that the PDF is really creat    ed (at the end of the code).
- [ ] Check if the zipped folder must really be `python` for it to work on AWS Lambda.
- [ ] There was a blog that hinted me for the MacOS binary compilation problem, I am not sure if it is the one below. Confirm this.


#### References
- Main reference for the binary targeting issue: https://repost.aws/knowledge-center/lambda-python-package-compatible. This was the page that hinted for the MacOS-specific compilation errors.
- Solution that was not used (using pre-configured layers from AWS that included Numpy and Pandas): https://stackoverflow.com/questions/46185297/using-numpy-in-aws-lambda