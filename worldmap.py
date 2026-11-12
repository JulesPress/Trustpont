import plotly.graph_objects as go

# Country centroids (lat, lon) for the countries the prototype knows about.
CENTROIDS = {
    "Austria": (47.6, 14.5), "Belgium": (50.6, 4.6), "Bulgaria": (42.7, 25.2), "Croatia": (45.1, 16.0), "Czechia": (49.8, 15.5),
    "Denmark": (56.1, 9.5), "Estonia": (58.7, 25.5), "Finland": (63.5, 26.0), "France": (46.7, 2.4), "Germany": (51.1, 10.3),
    "Greece": (39.0, 22.9), "Hungary": (47.2, 19.5), "Ireland": (53.2, -8.0), "Italy": (42.5, 12.5), "Latvia": (56.9, 24.8),
    "Lithuania": (55.3, 23.9), "Netherlands": (52.2, 5.3), "Norway": (61.0, 9.0), "Poland": (52.0, 19.4), "Portugal": (39.6, -8.0),
    "Romania": (45.9, 25.0), "Slovakia": (48.7, 19.5), "Slovenia": (46.1, 14.8), "Spain": (40.2, -3.7), "Sweden": (62.0, 16.0),
    "Switzerland": (46.8, 8.2), "United Kingdom": (54.0, -2.5), "Luxembourg": (49.8, 6.1), "Iceland": (64.9, -18.5),
}

SATELLITE = "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"


def build(by_country, picked, role, theme="warm"):
    """Satellite basemap of Europe. One pin per country: size = number of profiles, colour = best match."""
    cds = [c for c in by_country if c in CENTROIDS]
    lat = [CENTROIDS[c][0] for c in cds]
    lon = [CENTROIDS[c][1] for c in cds]
    best = [max(r[0]["mutual"] for r in by_country[c]) for c in cds]
    hi = "#C6E6A0" if theme != "azure" else "#4C86FF"
    col = [hi if b > 75 else "#FFFFFF" if b >= 50 else "#C9D0DC" for b in best]
    size = [13 + 3 * min(len(by_country[c]) - 1, 4) for c in cds]
    label = [f"\u2003\u2003{c}\u00a0\u00a0{b}" + (f"\u00a0·\u00a0{len(by_country[c])}" if len(by_country[c]) > 1 else "") for c, b in zip(cds, best)]
    hover = [f"<b>{c}</b><br>{len(by_country[c])} profile{'s' if len(by_country[c]) > 1 else ''} · best match {b}" for c, b in zip(cds, best)]
    fig = go.Figure()
    # two soft halos give a calm pulse-like glow; the selected pin gets a wider one
    fig.add_trace(go.Scattermap(lat=lat, lon=lon, mode="markers", hoverinfo="skip", marker=dict(size=[s + (46 if c == picked else 30) for s, c in zip(size, cds)], color=col, opacity=0.14)))
    fig.add_trace(go.Scattermap(lat=lat, lon=lon, mode="markers", hoverinfo="skip", marker=dict(size=[s + (26 if c == picked else 16) for s, c in zip(size, cds)], color=col, opacity=0.30)))
    # white ring, then the coloured core on top
    fig.add_trace(go.Scattermap(lat=lat, lon=lon, mode="markers", hoverinfo="skip", marker=dict(size=[s + 6 for s in size], color="#FFFFFF", opacity=1)))
    fig.add_trace(go.Scattermap(lat=lat, lon=lon, customdata=cds, hovertext=hover, hoverinfo="text", mode="markers", marker=dict(size=size, color=col, opacity=1),
                                selected=dict(marker=dict(opacity=1)), unselected=dict(marker=dict(opacity=1))))
    # labels live on an invisible, bigger marker so the text clears the dot
    fig.add_trace(go.Scattermap(lat=lat, lon=lon, mode="markers+text", hoverinfo="skip", text=[l.replace("\u2003", "") for l in label], textposition="middle right",
                                textfont=dict(color="#FFFFFF", size=13), marker=dict(size=[s + 22 for s in size], color="rgba(0,0,0,0)", opacity=0)))
    center = dict(lat=CENTROIDS[picked][0], lon=CENTROIDS[picked][1]) if picked in CENTROIDS else dict(lat=50.2, lon=11.0)
    fig.update_layout(
        map=dict(style="white-bg", center=center, zoom=5.2 if picked in CENTROIDS else 3.55,
                 layers=[dict(sourcetype="raster", source=[SATELLITE], below="traces", opacity=0.72)]),
        font=dict(family='-apple-system, BlinkMacSystemFont, "SF Pro Text", system-ui, sans-serif'), margin=dict(l=0, r=0, t=0, b=0), paper_bgcolor="rgba(0,0,0,0)", showlegend=False, autosize=True, height=1000, clickmode="event+select",
        hoverlabel=dict(bgcolor="#10182B", font_color="#FFFFFF", bordercolor="rgba(255,255,255,0.3)"))
    return fig
