function normalizeIdentifier(input) {
  return String(input).trim();
}

function getCookie(name) {
  const value = `; ${document.cookie}`;
  const parts = value.split(`; ${name}=`);
  if (parts.length === 2) {
    return parts.pop().split(";").shift();
  }
  return null;
}

module.exports = {
  normalizeIdentifier,
  getCookie,
};
