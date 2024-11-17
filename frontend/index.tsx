import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as AppRouter, Route, Switch } from 'react-router-dom';
import axios from 'axios';
import HomePage from './HomePage';
import AboutPage from './AboutPage';
import PageNotFound from './PageNotFound';

axios.defaults.baseURL = process.env.REACT_APP_API_BASE_URL;

ReactDOM.render(
  <React.StrictMode>
    <AppRouter>
      <Switch>
        <Route exact path="/" component={HomePage} />
        <Route path="/about" component={AboutPage} />
        <Route component={PageNotFound} />
      </Switch>
    </AppRouter>
  </React.StrictMode>,
  document.getElementById('root')
);