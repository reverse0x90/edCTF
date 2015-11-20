import Ember from 'ember';

export function isSolved(params, hash) {
  var challengeId = parseInt(hash.id);
  var solvedChallengeList = hash.solved;
  return solvedChallengeList && (solvedChallengeList.indexOf(challengeId) >= 0);
}

export default Ember.Helper.helper(isSolved);
