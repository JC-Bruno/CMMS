import { BrowserRouter, Route, Routes } from "react-router-dom";

import { AppLayout } from "../layouts/AppLayout";
import { AssetsListPage } from "../../modules/assets/pages/AssetsListPage";
import { DashboardPage } from "../../modules/dashboard/pages/DashboardPage";
import { InventoryPage } from "../../modules/inventory/pages/InventoryPage";
import { MaintenanceRequestsListPage } from "../../modules/maintenance-requests/pages/MaintenanceRequestsListPage";
import { SettingsPage } from "../../modules/settings/pages/SettingsPage";
import { WorkOrdersListPage } from "../../modules/work-orders/pages/WorkOrdersListPage";
import { PageHeader } from "../../shared/components/PageHeader";

function NotFoundPage() {
  return (
    <section className="page">
      <PageHeader
        eyebrow="Error 404"
        title="Página no encontrada"
        description="La ruta solicitada no existe dentro del CMMS."
      />
    </section>
  );
}

export function AppRouter() {
  return (
    <BrowserRouter>
      <Routes>
        <Route element={<AppLayout />}>
          <Route index element={<DashboardPage />} />
          <Route path="assets" element={<AssetsListPage />} />
          <Route
            path="maintenance-requests"
            element={<MaintenanceRequestsListPage />}
          />
          <Route path="work-orders" element={<WorkOrdersListPage />} />
          <Route path="inventory" element={<InventoryPage />} />
          <Route path="settings" element={<SettingsPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}