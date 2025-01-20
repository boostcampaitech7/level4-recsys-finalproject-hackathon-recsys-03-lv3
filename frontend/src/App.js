import React, { useEffect, useState } from "react";
import AppRouter from './pages/Router';

const App = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/")
      .then((response) => response.json())
      .then((data) => setMessage(data.message));
      //.catch((error) => console.error("Error fetching data:", error));
  }, []);

  return (
    <div>
        {/* 라우터 컴포넌트*/}
        <AppRouter />
        <p>{message}</p>
    </div>
  );
}

export default App;