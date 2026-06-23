import type { AssetStructureNodeListItem } from "../types";

type AssetStructureTreeProps = {
  nodes: AssetStructureNodeListItem[];
};

function humanizeNodeType(nodeType: AssetStructureNodeListItem["node_type"]) {
  if (nodeType === "subsystem") {
    return "Subsistema";
  }

  if (nodeType === "component") {
    return "Componente";
  }

  return "Punto mantenible";
}

function renderNode(
  node: AssetStructureNodeListItem,
  childrenByParent: Map<string | null, AssetStructureNodeListItem[]>,
) {
  const children = childrenByParent.get(node.id) || [];

  return (
    <li className="asset-tree__item" key={node.id}>
      <div className="asset-tree__node">
        <div>
          <p className="asset-tree__code">{node.code}</p>
          <h4 className="asset-tree__name">{node.name}</h4>
        </div>

        <div className="asset-tree__meta">
          <span>{humanizeNodeType(node.node_type)}</span>
          {node.is_maintainable ? <strong>Mantenible</strong> : null}
        </div>
      </div>

      {children.length > 0 ? (
        <ul className="asset-tree__children">
          {children.map((child) => renderNode(child, childrenByParent))}
        </ul>
      ) : null}
    </li>
  );
}

export function AssetStructureTree({ nodes }: AssetStructureTreeProps) {
  const nodesByAsset = new Map<string, AssetStructureNodeListItem[]>();

  nodes.forEach((node) => {
    const assetKey = node.asset;
    const assetNodes = nodesByAsset.get(assetKey) || [];

    assetNodes.push(node);
    nodesByAsset.set(assetKey, assetNodes);
  });

  return (
    <div className="asset-structure">
      {[...nodesByAsset.entries()].map(([assetId, assetNodes]) => {
        const firstNode = assetNodes[0];
        const childrenByParent = new Map<
          string | null,
          AssetStructureNodeListItem[]
        >();

        assetNodes.forEach((node) => {
          const parentKey = node.parent || null;
          const siblings = childrenByParent.get(parentKey) || [];

          siblings.push(node);
          childrenByParent.set(parentKey, siblings);
        });

        const rootNodes = childrenByParent.get(null) || [];

        return (
          <article className="asset-structure__group" key={assetId}>
            <div className="asset-structure__header">
              <p className="asset-structure__asset-code">
                {firstNode.asset_code || "Activo"}
              </p>
              <h3 className="asset-structure__asset-name">
                {firstNode.asset_name || "Activo sin nombre"}
              </h3>
            </div>

            <ul className="asset-tree">
              {rootNodes.map((node) => renderNode(node, childrenByParent))}
            </ul>
          </article>
        );
      })}
    </div>
  );
}