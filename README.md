# EISWebFit
This is a simple (and ugly) Flask app that showcases how easy it is to make a simple web application for fitting electrochemical impedance data. It also shows how Plotly Dash can be embedded into a Flask app, instead of taking control of the entire command flow. As an added bonus, it also contains a small script for generating noiseless, simulated electrochemical impedance data.

### How to use EISWebFit
1. Clone the repository and install the dependencies.
2. Put your impedance data in the EISWebFit/data folder. The impedance data is expected to be in three columns, frequency, real impedance, and complex impedance; and the frequencies should be in ascending order. See one of the existing data files for an example.
3. If you would like to fit a non-standard circuit, add it to the circuitOptions list in the dashboard.py file.
3. Run wsgi.py from the command line, and navigate to the provided IP address on your preferred web browser.
4. Choose a data file, choose a circuit, provide some initial guesses, and fit!
