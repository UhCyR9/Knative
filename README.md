# Knative

## Wprowadzenie

Knative to niezależne od platformy rozwiązanie stworzone z myślą o budowaniu, wdrażaniu i zarządzaniu skalowalnymi aplikacjami w kontenerach,
które są uruchamiane na infrastrukturze Kubernetes. Celem Knative jest ułatwienie i automatyzacja wielu aspektów zarządzania kontenerami, takich jak wdrażanie aplikacji,
zarządzanie ruchem sieciowym oraz łączenie usług. Knative zaprojektowano z myślą o rozszerzalności i integracji z istniejącymi narzędziami i usługami w ekosystemie Kubernetes.
Dzięki temu deweloperzy mogą skoncentrować się na pisaniu kodu aplikacji, nie martwiąc się o infrastrukturę,
co przyspiesza proces wdrażania aplikacji i ułatwia zarządzanie ich cyklem życia.

## Podstawy teoretyczne i stos technologiczny

Knative opiera się na 3 głównych filarach:
* **Budowa (Build)** \
Knative oferuje narzędzia do automatycznego budowania obrazów kontenerów bezpośrednio z kodu źródłowego przechowywanego w repozytorium git.
* **Obsługa serwerów (Serving)** \
Kluczowe zasoby Knative Serving obejmują Usługi (Services), Trasy (Routes), Konfiguracje (Configurations) oraz Rewizje (Revisions). Usługa w Knative automatycznie zarządza całym cyklem życia obciążenia pracy, kontrolując tworzenie innych obiektów.
Trasy umożliwiają mapowanie punktów końcowych sieci do jednej lub więcej rewizji, pozwalając zarządzać ruchem na wiele sposobów. Konfiguracje utrzymują pożądany stan wdrożenia, oddzielając kod od konfiguracji i umożliwiając tworzenie nowych rewizji przez modyfikację konfiguracji. Rewizje są niezmiennymi migawkami kodu i konfiguracji dla każdej modyfikacji obciążenia pracy, które mogą być automatycznie skalowane w zależności od ruchu przychodzącego.

