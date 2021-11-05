<h2 align="center">Mad Maids Table</h2>

<p align="center">
<a href="https://github.com/mad-maids/maid.hub"><img src="https://img.shields.io/static/v1.svg?style=flat-square&label=maid.hub&message=synced&logoColor=eceff4&logo=github&colorA=000000&colorB=ffffff"/></a>
<a href="https://github.com/mad-maids/maid.ts"><img src="https://img.shields.io/static/v1.svg?style=flat-square&label=maid.ts&message=synced&logoColor=eceff4&logo=github&colorA=000000&colorB=ffffff"/></a>
</p>

<p align="center">
<a href="https://github.com/mad-maids/maid.table/actions/workflows/build.yml"><img src="https://github.com/mad-maids/maid.table/actions/workflows/build.yml/badge.svg?branch=main"/></a>
</p>

**Big thanks to [Durbek Kamolov](https://github.com/DurbeKK) for creating
automations and contributing to Mad Maids. This project came true thanks for its
contributors participated on our projects...**

**This project serves as a timetable database for Mad Maids projects. Editing
this repository changes the database to all repositories.**

## For Timetable Editors

Keep in mind that a single mistake may break all our applications. So, in order
to avoid this, we added a formatter to our project. In order to format and fix
mistakes, make sure you have `Node.js` and `Yarn` installed on your computer.
Then, run these commands below:

```shell
# Install all required dependencies
yarn install

# Start formatting
yarn format

# (Optional) If you would like to check for format issues
yarn format:check
```

### Extra Notes

If you'd like to use the `get_jsons.py` script to update the `.json` files,
first make sure that you have `Python` and
[`ChromeDriver`](https://sites.google.com/chromium.org/driver/downloads?authuser=0)
installed on your computer (if you are using Windows, make sure to move the
`chromedriver.exe` to the working directory). Then, create and activate a
virtual environment and install the required packages with the following
command:

```shell
python3 -m pip install -r requirements.txt
```

Finally, change the variables in the `.env.example` file and rename it to
`.env`. Run the script with the following command:

```shell
python3 get_jsons.py
```

Once the script finishes running, test the output `.json` files by running this
command:

```shell
pytest -q test_jsons.py
```

---

> The project is being actively edited in order to keep the latest information,
> if you found our information outdated, please
> [open issues](https://github.com/mad-maids/maid.table/issues/new) and let us
> know about it.

<p align="center">Copyright &copy; 2021 <a href="https://maid.uz" target="_blank">Mad Maids</a></p>

<p align="center"><a href="https://github.com/mad-maids/maid.table/blob/master/license"><img src="https://img.shields.io/static/v1.svg?style=flat-square&label=License&message=MIT&logoColor=eceff4&logo=github&colorA=000000&colorB=ffffff"/></a></p>
