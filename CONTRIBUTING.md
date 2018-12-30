# Contributing to klvdata

## Welcome

Our project is open to contributors. A Contributor is a volunteer who promotes the project by granting services and data to the project. Contributors are recognized in [CONTRIBUTORS.md](https://github.com/paretech/klvdata/blob/master/CONTRIBUTORS.md). Our project depends on contributors, so a big thank you for your interest. Still here? Then Welcome to the team! [Fork klvdata on GitHub](https://github.com/paretech/klvdata/fork) and let's get started.

## In a Nutshell

Practicality beats purity, the main points are to not infringe upon the intellectual property of others; keep the master branch deploy ready; resist making changes that are not in scope; and mitigate the introduction of bugs by using and cultivating our automated test suite. Our team is comprised of volunteers with limited time so we seek high quality pull requests that leverage our infrastructure.

## Infrastructure

The project uses Travis CI to [automatically test](https://travis-ci.org/paretech/klvdata) and [build documentation](https://paretech.github.io/klvdata/) (gh-pages branch). Coveralls is used to [analyze test coverage](https://coveralls.io/github/paretech/klvdata). The master branch is always "deploy ready." Official releases are generated from the master branch and posted manually to the [Python Package Index (PyPI)](https://pypi.org/project/klvdata/). The project uses [semantic versioning](https://semver.org/).

## Change Process

Our change process is based on branches and pull requests.

1. Propose change and seek assignment using issues
2. Create branch on fork
3. Test and develop branch
4. Test and review branch
5. Push to fork and submit pull request
6. Respond to reviewer comments on branch
7. Repeat until pull request accepted and merged
8. Delete branch

## Issues

Changes to the project start life as an issue in the [issue tracker](https://github.com/paretech/klvdata/issues). Issues are labeled as a &quot;bug&quot; or &quot;enhancement.&quot; Issues are used to propose, accept and track development. When an issue is approved, it is assigned to a contributor for promotion.

## Local Environment

After an issue is approved, create a branch on the fork dedicated to the issue. Clone the branch locally, create and activate a virtual environment. Using the newly created environment, verify the existing test suite runs without incident (i.e. no errors or failures). If the test suite runs without incident, it is a healthy sign and development can proceed.

## Commits

Commits should be small, frequent, and accompanied by a [detailed message](https://chris.beams.io/posts/git-commit/). Commits should be within scope of the issue. Commits should include tests that demonstrate they works as proposed. Commits should not break existing tests. Commits should follow [Python&#39;s documentation style guide](https://devguide.python.org/documenting/). Commits should follow [Python&#39;s PEP 8 style guide](https://www.python.org/dev/peps/pep-0008/).

## Pull Requests

[Pull Requests](https://github.com/paretech/klvdata/pulls) are [created from a fork](https://help.github.com/articles/creating-a-pull-request-from-a-fork/) when work has been done to promote an issue. The pull request should include an [issue reference](https://help.github.com/articles/autolinked-references-and-urls/) in the body. If your name isn't already in [CONTRIBUTORS.md](https://github.com/paretech/klvdata/blob/master/CONTRIBUTORS.md), please add that change to the pull request to be recognized. Review and cleanup the commit history prior to submitting pull request. Refrain from submitting a pull request until after the test suite runs without incident in the local environment. Refrain from submitting a pull request that does not include tests that demonstrate the pull request works as proposed.

## Contributor Requirements

1. The Contributor **shall** ensure the services and data they grant to the klvdata project are legally theirs to give and do not infringe upon the intellectual property of others.

## Review Process

After a pull request is received, a [collaborator](https://api.github.com/repos/paretech/klvdata/contributors?page=1&amp;?access_token=fff) will review the pull request history, review and execute the tests used to ensure that the pull request performs as proposed, and that the pull request generally satisfies the quality guidelines outlined in this document. The reviewer will most likely make comments about how it can be improved. It is expected that the pull request be updated to resolve the comments. At the conclusion of the review and correction process, the pull request will be accepted and merged with the master branch. The pull request is merged using the “squash and merge” method. The approving reviewer will close the relevant issue and the contributor can delete the branch on their fork.

## Resources

### Project Specific

- [klvdata Repository (GitHub)](https://github.com/paretech/klvdata)
- [klvdata Issue Tracker (GitHub)](https://github.com/paretech/klvdata/issues)
- [klvdata Documentation (GitHub)](https://paretech.github.io/klvdata/)
- [klvdata Test and Deployment (Travis CI)](https://travis-ci.org/paretech/klvdata)
- [klvdata Code Coverage Metrics (Coveralls)](https://coveralls.io/github/paretech/klvdata)
- [klvdata Official Releases (PyPI)](https://pypi.org/project/klvdata/)

### Relevant Standards

- Motion Imagery Standards Board (MISB) [Standards (ST)](http://www.gwg.nga.mil/misb/st_pubs.html) and [Recommended Practices (RP)](http://www.gwg.nga.mil/misb/rp_pubs.html)
  - ST 0601 UAS Datalink Local Set
  - ST 1402 MPEG-2 Transport Stream for Class 1/Class 2 Motion Imagery, Audio and Metadata
  - ST 0902 Motion Imagery Sensor Minimum Metadata Set
  - ST 0107 Bit and Byte Order for Metadata in Motion Imagery Files and Streams
  - ST 0102 Security Metadata Universal and Local Sets for Motion Imagery Data
  - RP 0904 H.264 Bandwidth/Quality/Latency Tradeoffs
  - RP 0701 Common Metadata System: Structure

- SMPTE ST 336 Data Encoding Protocol using Key-Length-Value

- ISO/IEC 13818-1 Information technology — Generic coding of moving pictures and associated audio information: Systems

### Relevant Software

While this project has no affiliation with the following resources, they may of interest and practical benefit to users and contributors.

- [FFmpeg](https://www.ffmpeg.org/)
- [VLC media player](https://www.videolan.org)
- [TSDuck](https://tsduck.io/)
- [gstreamer](https://gstreamer.freedesktop.org/)
- [droneklv](https://github.com/wiseman/droneklv)
- [QGIS](https://qgis.org/en/site/index.html)
- [PAR Gv3.0](https://www.pargovernment.com/topic_details.asp?key=71)