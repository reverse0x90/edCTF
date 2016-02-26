import Ember from 'ember';

export function ifEqual(params/*, hash*/) {
  return params[0] === params[1];
}

export default Ember.Helper.helper(ifEqual);
