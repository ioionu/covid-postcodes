const DEFAULT_POSTCODES = [2017];
const ACTIVE_POSTCODES = new Set();
const DAYS = 5;

const fetchPostcodes = async handleClick => {
  const resp = await fetch("/api/v1/postcodes")
  const data = await resp.json();
  const lgas = data.reduce((reducer, lga) => {
    if (lga[0].length === 0 || lga[1].length === 0) {
      return reducer;
    }
    if (!(lga[1] in reducer)) {
      reducer[lga[1]] = [];
    }
    reducer[lga[1]].push(lga[0]);
    return reducer;
  }, {});

  console.log("postcodes", data, lgas);
  const selectors = document.createElement("ul");
  for (let [lga, lgaPostcodes] of Object.entries(lgas)) {
    const li = document.createElement("li");
    const lgaLabel = document.createElement("div");
    lgaLabel.appendChild(document.createTextNode(lga));
    lgaLabel.addEventListener("click", (event) => handleClick(event, lgaPostcodes))
    li.appendChild(lgaLabel);
    const ul = document.createElement("ul");
    lgaPostcodes.forEach(postcode => {

      // Create postcode elements.
      const pcli = document.createElement("li");
      const pcLabel = document.createElement("label");
      const pcCheckbox = document.createElement("input");
      const checkboxLabelId = `postcode-${postcode}`;

      // Setup elements.
      pcCheckbox.setAttribute("type", "checkbox");
      pcCheckbox.setAttribute("id", checkboxLabelId);
      pcLabel.setAttribute("for", checkboxLabelId);
      pcCheckbox.addEventListener('click', (event) => handleClick(event, [postcode]));
      pcCheckbox.value = postcode;

      // Stack elements.
      pcLabel.appendChild(document.createTextNode(postcode));
      pcli.appendChild(pcCheckbox);
      pcli.appendChild(pcLabel);
      ul.appendChild(pcli);
    });
    li.appendChild(ul);
    selectors.appendChild(li);
  }
  document.getElementById("postcodes").appendChild(selectors);
};

const fetchCases = async postcodes => {
  const resp = await fetch("/api/v1/cases", {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json;charset=utf-8'
    },
    body: JSON.stringify({
      postcodes
    })
  });
  return await resp.json();
};

const updateChart = (chart, { linked, unlinked, average, x }) => {

  const chartData = {
    type: "bar",
    types: {
      average: "line",
    },
    x: "x",
    columns: [
      ["x", ...x],
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
      "average": `${DAYS} day average`,
    }  
  };

  chart.load(chartData);

  // Todo: find a cleaner way to set the title or atleast a less crazy
  // selector.
  const title = chart.$.chart._groups[0][0].querySelector(".bb-title");
  title.textContent = `Covid cases in postcode(s) ${[...ACTIVE_POSTCODES]}`;
};

const transformData = data => {
  const unlinked = [...data.map(day => day[1] === null ? 0 : day[1])];
  const linked = [...data.map(day => day[2] === null ? 0 : day[2])];
  const total = [...data.map(day => day[1] + day[2])];

  // Calculate moving average.
  const average = new Array(DAYS);
  average.fill(null);
  for (let i = 5; i < total.length; i++) {
    average.push(
      total.slice(i - DAYS, i)
        .reduce(
          (reducer, value) => reducer + value
        )
      / DAYS
    );
  }

  // x axis values (ie dates).
  const x = [...data.map(day => day[0])]
  return { linked, unlinked, average, x };
};

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

    const data = await fetchCases(postcodes);
    console.log(data);
    const { linked, unlinked, average, x } = transformData(data);
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
            ["x", ...x],
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
            "average": `${DAYS} day average`,
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

    const handleClick = async (event, postcodes) => {
      for (postcode of postcodes) {
        ACTIVE_POSTCODES.has(postcode)
          ? ACTIVE_POSTCODES.delete(postcode)
          : ACTIVE_POSTCODES.add(postcode);
      }
      console.log(event, ACTIVE_POSTCODES);
      const fetchedData = await fetchCases([...ACTIVE_POSTCODES]);
      const transformedData = transformData(fetchedData);
      updateChart(
        chart,
        transformedData
      );

      // Update checkboxes.
      document.querySelectorAll("#postcodes input").forEach(input => {
        ACTIVE_POSTCODES.has(input.value)
          ? input.checked = true
          : input.checked = false;
      });

      // Update URL.
      const url = new URL(window.location);
      url.searchParams.set('postcodes', [...ACTIVE_POSTCODES]);
      history.pushState({}, '', url);
    };

    await fetchPostcodes(handleClick);
};

app();



