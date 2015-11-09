
try:
    import artifactory_utils
except:
    pass
else:
    dependencies = [
        artifactory_utils.ArtifactSelector(
            project="Toolchain-Release",
            revision="develop",
            debug=False,
            stable_required=True),
        artifactory_utils.ArtifactSelector(
            project="Python3.4",
            revision="develop",
            debug=False,
            stable_required=True),
        artifactory_utils.ArtifactSelector(
            project="EmbeddedPython",
            revision="develop",
            debug=False,
            stable_required=True)
    ]
