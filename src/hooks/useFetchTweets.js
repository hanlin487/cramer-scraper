import { useState, useEffect } from "react";

function useFetchTweets() {
  const [tweets, setTweets] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function pullDB() {
      try {
        const res = await fetch("http://localhost:3000/data");
        const data = await res.json();
        setTweets(data.reverse());
        setLoading(false);
      } catch (E) {
        console.error(`pullDB Error ${E}`);
        setError(E.message);
        setLoading(false);
      }
    }

    pullDB();
  }, []); // empty dependency array so it only runs once

  return { tweets, loading, error };
}

export default useFetchTweets;
