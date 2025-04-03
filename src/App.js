import "./App.css";

function App() {
  return (
    <div className="App">
      Cramer Tweets
      <div className="button-container">
        <button onClick={log} id="week" className="btn">
          1 week
        </button>
        <button onClick={log} id="month" className="btn">
          1 month
        </button>
        <button onClick={log} id="year" className="btn">
          1 year
        </button>
        <button onClick={pullDB} id="fetch" className="btn">
          Fetch!
        </button>
      </div>
    </div>
  );
}
export default App;

function log(event) {
  console.log(`${event.target.id} button clicked`);
}

async function pullDB() {
  try {
    const res = await fetch("http://localhost:3000/data");
    const data = await res.json();
    console.log("Data fetched from the database:", data);
  } catch (E) {
    console.error(`pullDB Error ${E}`);
  }
}
