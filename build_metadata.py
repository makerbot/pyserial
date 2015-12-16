
try:
    import artifactory_utils
except:
    pass
else:
    dependencies = [
        artifactory_utils.ArtifactSelector(
            project="Toolchain-Release",
            revision="master",
            version="3.9.*",
            debug=False,
            stable_required=True),
        artifactory_utils.ArtifactSelector(
            project="Python3.4",
            revision="develop",
            debug=False,
            stable_required=True),
        artifactory_utils.ArtifactSelector(
            project="EmbeddedPython",
            revision="master",
            version="0.1.*",
            debug=False,
            stable_required=True)
    ]
