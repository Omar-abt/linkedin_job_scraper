import React from 'react';
import './App.css';
import reactLogo from './assets/react.svg';
import viteLogo from '/vite.svg';

function App() {
  const formData = new FormData();
  formData.append('job_name', 'Software Engineer');
  formData.append('job_location', 'Ottawa');

  const callApi = async () => {
    try {
      const response = await fetch(
        `${import.meta.env.VITE_APP_BACKEND_BASE_URL}/scraper`,
        {
          method: 'POST',
          body: formData,
        }
      );

      // Handle success
      console.log('POST request sent successfully');
      return response;
    } catch (error) {
      // Handle error
      console.error('There was an error:', error);
    }
  };

  return (
    <div>
      <button onClick={callApi}>Click here</button>
    </div>
    // <>
    //   <div>
    //     <a href="https://vitejs.dev" target="_blank">
    //       <img src={viteLogo} className="logo" alt="Vite logo" />
    //     </a>
    //     <a href="https://react.dev" target="_blank">
    //       <img src={reactLogo} className="logo react" alt="React logo" />
    //     </a>
    //   </div>
    //   <h1>Vite + React</h1>
    //   <div className="card">
    //     <button onClick={() => setCount((count) => count + 1)}>
    //       count is {count}
    //     </button>
    //     <p>
    //       Edit <code>src/App.tsx</code> and save to test HMR
    //     </p>
    //   </div>
    //   <p className="read-the-docs">
    //     Click on the Vite and React logos to learn more
    //   </p>
    // </>
  );
}

export default App;
