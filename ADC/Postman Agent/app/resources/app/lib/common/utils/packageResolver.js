const fs = require('fs');
const path = require('path');
const sanitizePackageId = require('./sanitizePackageId');

const PACKAGE_FILE_DIRECTORY = './scriptPackageFiles';

/**
 * PackageResolver class for resolving packages by fetching their contents from the cloud or using cached data.
 */
class PackageResolver {
  /**
   * Creates an instance of PackageResolver.
   */
  constructor (tempDirPath, collectionId) {
    // Initialize script content cache
    this.scriptContentCache = {};
    this.tempDirPath = tempDirPath;
    this.collectionId = collectionId;

    // Bind resolvePackages method to the current instance
    this.resolvePackages = this.resolvePackages.bind(this);
  }

  /**
   * Resolves packages by fetching their contents from the cloud or using cached data.
   * @param {Object} options - The options for resolving packages.
   * @param {Object} options.packages - The packages to resolve.
   * @param {Function} callback - The callback function to invoke when the resolution is complete.
   */
  resolvePackages ({ packages }, callback) {
    // Check if there are no packages to resolve
    if (!packages || !Object.keys(packages).length) {
      return callback(null, {});
    }

    if (!pm.wsPackageFetchService) {
      return callback(new Error('Package fetch service not available'));
    }

    let packagesToFetch = {};
    let cachedData = {};

    // Separate packages to fetch and cached packages
    Object.entries(packages).forEach(([packageName, packageData]) => {
      let fileExists = false;

      try {
        // Check if the package is saved locally in the temp directory
        // For more information: https://github.com/postman-eng/postman-app/pull/19641
        const filePath = `${PACKAGE_FILE_DIRECTORY}/${sanitizePackageId(packageData.id)}`;
        const tempFilePath = path.join(this.tempDirPath, filePath);
        fileExists = fs.existsSync(tempFilePath);


        if (!this.scriptContentCache[packageName]) {
          packagesToFetch[packageName] = { id: packageData.id, forceSave: !fileExists };
        } else {
          cachedData[packageName] = { data: this.scriptContentCache[packageName] };
        }
      } catch (error) {
        pm.logger.error('PackageResolver~resolvePackages: Error checking if package is saved locally', error);
      }

    });


    // If all packages are cached, return cached data immediately
    if (Object.keys(packagesToFetch).length === 0) {
      return callback(null, cachedData);
    }

    if (pm.wsPackageFetchService) {
      pm.wsPackageFetchService.fetchPackage(packagesToFetch, this.collectionId, (err, data, packageErrors) => {
        if (err) {
          return callback(err);
        }

        const fileData = this._processFetchedData(data, packageErrors);

        Object.assign(fileData, cachedData);

        callback(null, fileData);
      });
    }
  }

  /**
   * Processes fetched data from package events.
   * @param {Object} packages - The fetched data containing package names and file paths.
   * @param {Object} packageErrors - The errors encountered while fetching packages.
   * @returns {Object} An object containing package names as keys and file data as values.
   * @private
   */
  _processFetchedData (packages, packageErrors) {
    const fileData = {};
    Object.entries(packages).forEach(([packageName, filePath]) => {
      if (!filePath) {
        fileData[packageName] = { error: packageErrors?.[packageName] ?? `Cannot find Package ${packageName}` };
        pm.logger.error('PackageResolver~_processFetchedData: Error finding package', new Error(`No path found for package ${packageName}`));
        return;
      }
      try {
        filePath = path.join(this.tempDirPath, filePath);
        const fileContents = fs.readFileSync(filePath, 'utf8');

        fileData[packageName] = { data: fileContents };

        // Cache file contents
        this.scriptContentCache[packageName] = fileContents;
      } catch (error) {
        pm.logger.error('PackageResolver~_processFetchedData: Error reading file', error);
      }
    });

    return fileData;
  }
}

module.exports = PackageResolver;
