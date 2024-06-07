import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import './moarCss.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

ReactDOM.render(<App url={process.env.REACT_APP_BACKEND_URL}/>, document.getElementById('root'));

serviceWorker.unregister();