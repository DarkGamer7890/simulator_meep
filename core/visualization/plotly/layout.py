def apply_common_layout(fig, title, xlabel, ylabel, spatial):
    fig.update_layout(

        title=dict(
            text=title,
            x=0.5,
            xanchor="center",
            font=dict(color="black", size=16)
        ),
        height=600,
        margin=dict(l=40, r=40, t=60, b=40),
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        hovermode="x unified",

        font=dict(
            color="black",  
        ),

        xaxis=dict(
            title=dict(
                text=xlabel,
                font=dict(color="black"),
            ),
            showgrid=True,
            gridcolor="lightgray",
            linecolor="black",
            ticks="outside",
            tickfont=dict(color="black"),
            zeroline=False,
            # scaleanchor="y", 
            # scaleratio=1
        ),

        yaxis=dict(
            title=dict(
                text=ylabel,
                font=dict(color="black"),
            ),
            showgrid=True,
            gridcolor="lightgray",
            linecolor="black",
            ticks="outside",
            tickfont=dict(color="black"),
            zeroline=False,
            scaleanchor="x", 
            scaleratio=1
            # constrain="domain"
        ),
    )

    if spatial:
        fig.update_yaxes(autorange="reversed")