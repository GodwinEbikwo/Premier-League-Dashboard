import dash_loading_spinners as dls
from dash import html


def StatCardImage(title, title_id, style, icon_src):
    return html.Div(
        className=f"grid__card {style}",  # Adjust the class name as needed
        children=[
            html.Div(
                className="card-body",
                children=[
                    html.Div(
                        className="d-flex justify-content-between",
                        children=[
                            html.Div(
                                className="card-info w-100",
                                children=[
                                    html.Small(
                                        className="card-text",
                                        children=[title],  # Title of the card
                                    ),
                                    dls.Triangle(
                                        html.H2(
                                            className="mb-2 mt-2 card-title mb-2",
                                            id=f"{title_id}",
                                            children=[title_id],
                                            style={"font-size": "3vw"},
                                        ),
                                    ),
                                    html.Small(
                                        className="card-text",
                                        children=["In the 38 games"],
                                    ),
                                ],
                                style={"text-align": "center"},
                            ),
                            html.Div(
                                className="card-icon d-flex align-items-center w-50",
                                children=[
                                    html.Img(
                                        className="img-fluid bx-lg",
                                        src=icon_src,  # Path to the icon image
                                        style={"width": "4rem"},
                                    ),
                                ],
                            ),
                        ],
                    ),
                ],
            ),
        ],
    )
