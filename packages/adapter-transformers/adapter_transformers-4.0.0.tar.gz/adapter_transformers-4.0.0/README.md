<!---
Copyright 2020-2024 The AdapterHub Team. All rights reserved.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
-->

## ⚠️ IMPORTANT NOTE ⚠️

This is the legacy `adapter-transformers` library, which has been replaced by the new **Adapters library, found here: https://github.com/adapter-hub/adapters**.

- **⚠️ Beginning with version 4.0.0, the `adapter-transformers` package will automatically install the latest `adapters` package version instead. ⚠️**  
  From this version on, the `adapter-transformers` package does not contain any own functionality.
- Older versions of `adapter-transformers` are kept for archival purposes, and should not be used for active projects.

Install the new library directly via: `pip install adapters`.

The documentation of adapter-transformers can be found at https://docs-legacy.adapterhub.ml.
The documentation of the new _Adapters_ library can be found at https://docs.adapterhub.ml.
For transitioning, please read: https://docs.adapterhub.ml/transitioning.html.

---


<p align="center">
<img style="vertical-align:middle" src="https://raw.githubusercontent.com/Adapter-Hub/adapters/main/docs/img/adapter-bert.png" width="80" />
</p>
<h1 align="center">
<span><i>Adapters</i></span>
</h1>

<h3 align="center">
A Unified Library for Parameter-Efficient and Modular Transfer Learning
</h3>
<h3 align="center">
    <a href="https://adapterhub.ml">🌍 Website</a>
    &nbsp; • &nbsp;
    <a href="https://github.com/Adapter-Hub/adapters/tree/main/notebooks">💻 GitHub</a>
    &nbsp; • &nbsp;
    <a href="https://docs.adapterhub.ml">📚 Docs</a>
    &nbsp; • &nbsp;
    <a href="https://arxiv.org/abs/2311.11077">📜 Paper</a>
    &nbsp; • &nbsp;
    <a href="https://github.com/Adapter-Hub/adapters/tree/main/notebooks">🧪 Tutorials</a>
</h3>

_Adapters_ is an add-on library to [HuggingFace's Transformers](https://github.com/huggingface/transformers), integrating [various adapter methods](https://docs.adapterhub.ml/overview.html) into [state-of-the-art pre-trained language models](https://docs.adapterhub.ml/model_overview.html) with minimal coding overhead for training and inference.

```
pip install adapters
```
