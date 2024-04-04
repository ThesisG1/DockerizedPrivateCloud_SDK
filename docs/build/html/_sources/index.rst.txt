.. Drone Digital Twin SDK documentation master file, created by
   sphinx-quickstart on Thu Apr  4 16:45:14 2024.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Drone Digital Twin SDK's documentation!
==================================================

.. toctree::
   :maxdepth: 3
   :caption: Contents:
   
   setting_up
   dev_guide

Overview
===============
Building digital twins for drones is not a trivial task and it requires a specific pipeline to be followed. 
Our project aims to provide a Software Development Kit (SDK) that will help developers to build digital twins for drones.
The architecture of our project consists of three main Layer: 

1. **ROS Layer**: 
2. **Middleware Layer**: 
3. **Namespace**:

The project uses the concept of a dockerized private cloud to host the dashboard and the Namespace that establish the bidirectional communication aka the digital twin

See the :ref:`setting-up` for more information on getting started with the SDK.

User Guide
==================
See the :ref:`developer-guide` for more information on how to use the SDK.

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
