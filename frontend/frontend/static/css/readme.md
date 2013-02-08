**Regarding the css/ folder (this one) - I've only included Sass files (.scss) to begin with (this is not a mistake).**

This folder should contain the compiled css, but until we discuss further, I vote that we keep it out of the repository. This doesn't mean that I'm saying we should compile serverside, but that for the purposes of development everyone dealing with the css should have [Compass](http://compass-style.org/) installed anyway (point it to the static directory, it should work automatically). This will prevent it from constantly changing and also stop people from mistakenly editing it instead of the .scss files in the sass/ directory.

*So if you're wondering why the site is unstyled, it's because it's looking for app.css which doesn't exist yet (generate it!).*

Once we've talked this through, we can either add .css to the .gitignore or just shove them in here if we decide to do it that way.
