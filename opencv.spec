%global debug_package %{nil}
Name:           opencv
Version:        %{VERSION}
Release:        %{RELEASE}%{?dist}
Summary:        Collection of algorithms for computer vision
# This is normal three clause BSD.
License:        BSD
URL:            http://opencv.org

Source0:        %{name}-%{version}.tar.gz
Source1:        %{name}-contrib-%{version}.tar.gz

BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  cmake3
BuildRequires:  chrpath
BuildRequires:  eigen3-devel
BuildRequires:  gtk3-devel
BuildRequires:  libtheora-devel
BuildRequires:  libvorbis-devel
BuildRequires:  jasper-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  libGL-devel
BuildRequires:  libv4l-devel
BuildRequires:  OpenEXR-devel
BuildRequires:  zlib-devel
BuildRequires:  pylint
BuildRequires:  swig
BuildRequires:  libgphoto2-devel
BuildRequires:  libwebp-devel
BuildRequires:  tesseract-devel
BuildRequires:  protobuf-devel
BuildRequires:  glog-devel
BuildRequires:  doxygen
BuildRequires:  gflags-devel
BuildRequires:  libucil-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
BuildRequires:  hdf5-devel
BuildRequires:  openblas-devel
BuildRequires:  blas-devel
BuildRequires:  lapack-devel


Requires:       opencv-core%{_isa} = %{version}-%{release}

%description
OpenCV means Intel® Open Source Computer Vision Library. It is a collection of
C functions and a few C++ classes that implement some popular Image Processing
and Computer Vision algorithms.


%package        core
Summary:        OpenCV core libraries

%description    core
This package contains the OpenCV C/C++ core libraries.


%package        devel
Summary:        Development files for using the OpenCV library
Requires:       %{name}%{_isa} = %{version}-%{release}
Requires:       %{name}-contrib%{_isa} = %{version}-%{release}

%description    devel
This package contains the OpenCV C/C++ library and header files, as well as
documentation. It should be installed if you want to develop programs that
will use the OpenCV library. You should consider installing opencv-doc
package.


%package        doc
Summary:        docs files
Requires:       opencv-devel = %{version}-%{release}
BuildArch:      noarch
Provides:       %{name}-devel-docs = %{version}-%{release}
Obsoletes:      %{name}-devel-docs < %{version}-%{release}


%description    doc
This package contains the OpenCV documentation, samples and examples programs.


%package        contrib
Summary:        OpenCV contributed functionality

%description    contrib
This package is intended for development of so-called "extra" modules, contributed
functionality. New modules quite often do not have stable API, and they are not
well-tested. Thus, they shouldn't be released as a part of official OpenCV
distribution, since the library maintains binary compatibility, and tries
to provide decent performance and stability.

%prep
%setup -q -a1

%build
mkdir -p build
pushd build

cmake3 CMAKE_VERBOSE=1 \
 -DBUILD_TESTS=OFF \
 -DBUILD_PERF_TESTS=OFF \
 -DBUILD_EXAMPLES=OFF \
 -DWITH_IPP=OFF \
 -DWITH_ITT=OFF \
 -DWITH_QT=OFF \
 -DWITH_OPENGL=ON \
 -DOpenGL_GL_PREFERENCE=GLVND \
 -DWITH_GDAL=OFF \
 -DWITH_UNICAP=ON \
 -DCMAKE_SKIP_RPATH=ON \
 -DWITH_CAROTENE=OFF \
 -DENABLE_PRECOMPILED_HEADERS=OFF \
 -DCMAKE_BUILD_TYPE=RELEASE \
 -DBUILD_opencv_java=OFF \
 -DWITH_CUDA=ON \
 -DCUDA_ARCH_BIN=6.1 \
 -DCUDA_VERBOSE_BUILD=ON \
 -DCUDA_PROPAGATE_HOST_FLAGS=OFF \
 -DBUILD_DOCS=ON \
 -DBUILD_EXAMPLES=OFF \
 -DINSTALL_C_EXAMPLES=ON \
 -DINSTALL_PYTHON_EXAMPLES=ON \
 -DENABLE_PYLINT=ON \
 -DBUILD_PROTOBUF=OFF \
 -DPROTOBUF_UPDATE_FILES=ON \
 -DOPENCV_SKIP_PYTHON_LOADER=ON \
 -DOPENCV_EXTRA_MODULES_PATH=../opencv_contrib-%{VERSION}/modules \
 -DWITH_LIBV4L=ON \
 -DWITH_OPENMP=ON \
 -DBUILD_opencv_cudacodec=OFF \
 -DCMAKE_INSTALL_PREFIX=/usr \
 ..

%make_build VERBOSE=1

popd


%install
%make_install -C build
find %{buildroot} -name '*.la' -delete
rm -rf %{buildroot}%{_datadir}/opencv4/licenses/

%check
# Check fails since we don't support most video
# read/write capability and we don't provide a display
# ARGS=-V increases output verbosity
# Make test is unavailble as of 2.3.1
#ifnarch ppc64
%if %{with tests}
pushd build
    LD_LIBRARY_PATH=%{_builddir}/%{name}-%{version}/build/lib:$LD_LIBARY_PATH make test ARGS=-V || :
popd
%endif
#endif

%post core
ldconfig

%postun core
ldconfig

%post contrib
ldconfig

%postun contrib
ldconfig

%files
%doc README.md
%license LICENSE
%{_bindir}/opencv_*
%{_bindir}/setup_vars_opencv4.sh
%dir %{_datadir}/opencv4
%{_datadir}/opencv4/haarcascades
%{_datadir}/opencv4/lbpcascades
%{_datadir}/opencv4/valgrind*
%{_datadir}/licenses/opencv4

%files core
%{_libdir}/libopencv_core.so.*
%{_libdir}/libopencv_features2d.so.*
%{_libdir}/libopencv_flann.so.*
%{_libdir}/libopencv_hfs.so.*
%{_libdir}/libopencv_highgui.so.*
%{_libdir}/libopencv_imgcodecs.so.*
%{_libdir}/libopencv_imgproc.so.*
%{_libdir}/libopencv_ml.so.*
%{_libdir}/libopencv_objdetect.so.*
%{_libdir}/libopencv_photo.so.*
%{_libdir}/libopencv_shape.so.*
%{_libdir}/libopencv_stitching.so.*
%{_libdir}/libopencv_superres.so.*
%{_libdir}/libopencv_video.so.*
%{_libdir}/libopencv_videoio.so.*
%{_libdir}/libopencv_videostab.so.*

%files devel
%{_includedir}/opencv4
%{_libdir}/lib*.so
%{_libdir}/cmake/opencv4/*.cmake

%files doc
%{_datadir}/opencv4/

%files contrib
%{_libdir}/libopencv_alphamat.so.*
%{_libdir}/libopencv_aruco.so.*
%{_libdir}/libopencv_bgsegm.so.*
%{_libdir}/libopencv_bioinspired.so.*
%{_libdir}/libopencv_calib3d.so.*
%{_libdir}/libopencv_ccalib.so.*
%{_libdir}/libopencv_cuda*.so.*
%{_libdir}/libopencv_cudev.so.*
%{_libdir}/libopencv_datasets.so.*
%{_libdir}/libopencv_dnn.so.*
%{_libdir}/libopencv_dnn_superres.so.*
%{_libdir}/libopencv_dnn_objdetect.so.*
%{_libdir}/libopencv_dpm.so.*
%{_libdir}/libopencv_face.so.*
%{_libdir}/libopencv_freetype.so.*
%{_libdir}/libopencv_fuzzy.so.*
%{_libdir}/libopencv_hdf.so.*
%{_libdir}/libopencv_gapi.so.*
%{_libdir}/libopencv_img_hash.so.*
%{_libdir}/libopencv_intensity_transform.so.*
%{_libdir}/libopencv_line_descriptor.so.*
%{_libdir}/libopencv_mcc.so.*
%{_libdir}/libopencv_optflow.so.*
%{_libdir}/libopencv_phase_unwrapping.so.*
%{_libdir}/libopencv_plot.so.*
%{_libdir}/libopencv_quality.so.*
%{_libdir}/libopencv_rapid.so.*
%{_libdir}/libopencv_reg.so.*
%{_libdir}/libopencv_rgbd.so.*
%{_libdir}/libopencv_saliency.so.*
%{_libdir}/libopencv_sfm.so.*
%{_libdir}/libopencv_stereo.so.*
%{_libdir}/libopencv_structured_light.so.*
%{_libdir}/libopencv_surface_matching.so.*
%{_libdir}/libopencv_text.so.*
%{_libdir}/libopencv_tracking.so.*
%{_libdir}/libopencv_wechat_qrcode.so.*
%{_libdir}/libopencv_xfeatures2d.so.*
%{_libdir}/libopencv_ximgproc.so.*
%{_libdir}/libopencv_xobjdetect.so.*
%{_libdir}/libopencv_xphoto.so.*
%{_libdir}/opencv4/3rdparty

%changelog

