const DEFAULT_POSTCODES = [2017];

const app = async () => {
    const url = new URL(window.location);
    const postcodesRaw = url.searchParams.get('postcodes');
    let postcodes = postcodesRaw === null
      ? []
      : postcodesRaw.split(',')
        .map(postcode => parseInt(postcode))
        .filter(postcode => postcode > 1999 && postcode < 3000);

      // If not postcodes found int URL, use default.
      if (postcodes.length === 0) {
        postcodes = DEFAULT_POSTCODES;
        url.searchParams.set('postcodes', postcodes);
        history.pushState({}, '', url);
      }

    const resp = await fetch("/api/v1/cases", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json;charset=utf-8'
        },
        body: JSON.stringify({
          postcodes
        })
    });
    const data = await resp.json();
    console.log(data);
    const unlinked = [...data.map(day => day[1] === null ? 0 : day[1])];
    const linked = [...data.map(day => day[2] === null ? 0 : day[2])];
    const total = [...data.map(day => day[1] + day[2])];

    // Calculate moving average.
    const days = 5;
    const average = new Array(days);
    average.fill(null);
    for (let i = 5; i < total.length; i++) {
      average.push(
        total.slice(i-days, i)
        .reduce(
          (reducer, value) => reducer+value
        )
        / days
      );
    }
    const chart = bb.generate({
      title: {
        text: `Covid cases in postcode(s) ${postcodes}`,
      },
      bindto: "#mountpoint",
      data: {
          type: "bar",
          types: {
            average: "line",
          },
          x: "x",
          columns: [
            ["x", ...data.map(day => day[0])],
            // ["total", ...total],
            ["linked", ...linked],
            ["unlinked", ...unlinked],
            ["average", ...average],
          ],
          groups: [
            [
              "linked", "unlinked",
            ]
          ],
          names:{
            "average": `${days} day average`,
          }  
      },
      axis: {
        x: {
          type: "timeseries",
          tick: {
            rotate: -90,
            format: "%Y-%m-%d",
          }
        }
      },
      grid: {
        x: {
          show: true
        },
        y: {
          show: true
        }
      },
  });
};

app();