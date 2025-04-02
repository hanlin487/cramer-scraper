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
      </div>
    </div>
  );
}

function log(event) {
  console.log(`${event.target.id} button clicked`);
}

export default App;
