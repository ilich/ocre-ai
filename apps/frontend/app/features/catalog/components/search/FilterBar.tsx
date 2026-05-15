import Box from "@mui/material/Box";
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import MenuItem from "@mui/material/MenuItem";
import Select from "@mui/material/Select";
import type { CatalogFilters, MetadataMap } from "../../types";

interface FilterConfig {
  key: keyof CatalogFilters;
  label: string;
}

const FILTERS: FilterConfig[] = [
  { key: "material", label: "Material" },
  { key: "denomination", label: "Denomination" },
  { key: "object_type", label: "Object Type" },
  { key: "manufacturer", label: "Manufacturer" },
  { key: "authority", label: "Authority" },
  { key: "geographic", label: "Mint Location" },
];

interface FilterBarProps {
  metadata: MetadataMap;
  filters: CatalogFilters;
  onChange: (filters: CatalogFilters) => void;
  disabled?: boolean;
}

export default function FilterBar({ metadata, filters, onChange, disabled }: FilterBarProps) {
  function handleChange(key: keyof CatalogFilters, value: string) {
    onChange({ ...filters, [key]: value });
  }

  return (
    <Box sx={{ display: "flex", flexWrap: "wrap", gap: 2 }}>
      {FILTERS.map(({ key, label }) => {
        const options = metadata[key] ?? [];
        return (
          <FormControl
            key={key}
            size="small"
            disabled={disabled || options.length === 0}
            sx={{ minWidth: 160 }}
          >
            <InputLabel>{label}</InputLabel>
            <Select
              label={label}
              value={filters[key]}
              onChange={(e) => handleChange(key, e.target.value)}
              MenuProps={{ slotProps: { paper: { sx: { maxHeight: 300 } } } }}
            >
              <MenuItem value="">
                <em>Any</em>
              </MenuItem>
              {options.map((opt) => (
                <MenuItem key={opt} value={opt}>
                  {opt}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        );
      })}
    </Box>
  );
}
