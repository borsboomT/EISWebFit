"""Plotly Dash HTML layout override."""

html_layout = """
<!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            <link rel="plotlyflask_tutorial\static\less" type="text/css" href="styles.less" />
            <script src="less.js-master\dist\less.js" type="text/javascript"></script>
            {%css%}
        </head>
        <body class="dash-template">
            <header>
              <div class="nav-wrapper">
                <a href="/">
                    <h1>Impedance Fitting App</h1>
                  </a>
                <nav>
                </nav>
            </div>
            </header>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
"""
