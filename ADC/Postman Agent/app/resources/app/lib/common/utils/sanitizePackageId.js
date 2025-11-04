const sanitizeFilename = require('sanitize-filename');

/**
 * Sanitizes a package ID to ensure valid folder and file name.
 *
 * External package IDs include invalid characters (e.g., 'npm:lodash@1.0.0'),
 * which cause issues when used directly as folder and file names.
 * This function replaces such characters (like ':' -> '-') to make the ID safe for filesystem operations.
 * The sanitized ID is returned in the format: sanitizedPackageID/sanitizedPackageID.
 *
 * Note: Scoped package IDs like 'npm:@faker-js/faker' are also handled,
 * resulting in sanitized value 'npm--faker-js-faker'.
 *
 * @param {string} packageId - The package ID to sanitize.
 * @returns {string} - Sanitized package ID in the format sanitizedPackageID/sanitizedPackageID.
 */
module.exports = function (packageId) {
  const sanitizedPackageID = sanitizeFilename(packageId, { replacement: '-' });

  return `${sanitizedPackageID}/${sanitizedPackageID}`;
};
