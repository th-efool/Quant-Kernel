# GUI Technical Documentation

This section documents the **custom UI framework layer** built on top of Tkinter.
These classes form the **foundation** that all higher-level UI logic (API selection, indicators, strategies, charts) depends on.

---

## 1️⃣ Base UI Abstractions

### `gui/components/base/base_ui_component.py`

```python
class UIComponent(ABC):
```

#### Purpose

Defines the **minimal contract** for every UI element in the system.

Every visible UI element **must**:

* Be buildable
* Expose a value (or explicitly return `None`)
* Own a root Tk widget

#### Key Fields

* `self.widget`:
  The **root Tk widget** of the component (Frame, LabelFrame, Button, etc.)
* `self.visible`:
  Logical visibility flag (used by `show()` / `hide()`)

#### Required Methods

* `build(parent)`

  * Creates all Tk widgets
  * Must assign `self.widget`
* `get_value()`

  * Returns structured data from the UI
  * Or `None` for renderer-only components

#### Optional Behavior

* `show()` / `hide()` manipulate widget stacking without destroying state

#### Why this matters

This abstraction allows:

* Components and layouts to be composed uniformly
* Layout containers to treat **components and other layouts identically**
* UI state to be read generically by the pipeline runner

---

## 2️⃣ Error Handling

### `gui/components/error.py`

```python
class InvalidInputFormat(ValueError)
```

#### Purpose

A **domain-specific exception** used when user input cannot be converted to the expected type.

#### Where used

* `ParamInputComponent`
* `SelectAndConfigure`
* `AddToListComponent`

#### Why not plain `ValueError`

Allows:

* Catching UI validation errors cleanly
* Displaying meaningful error dialogs
* Separating user errors from programmer errors

---

## 3️⃣ Parameter System

### `gui/components/param_spec.py`

```python
class ParamSpec:
```

#### Purpose

Defines a **parameter schema** for user input.

Each `ParamSpec` describes:

* Name
* Expected type
* Default value
* Whether it is optional

This decouples:

* UI layout
* Input validation
* Object construction

---

### `gui/components/param_input.py`

```python
class ParamInputComponent(UIComponent):
```

#### Purpose

Renders a **form UI** from a list of `ParamSpec` objects.

#### Responsibilities

* Render labeled input fields
* Handle default values
* Convert strings → typed Python values
* Raise `InvalidInputFormat` on failure

#### Output

```python
{
  "interval": 1,
  "from_date": "2025-01-01",
  "unit": Unit.days,
}
```

#### Why this exists

* Avoids writing custom Tkinter forms per config
* Allows strategy/indicator configs to be declared declaratively

---

## 4️⃣ Selection + Configuration

### `gui/components/select_and_configure.py`

```python
class SelectAndConfigure(UIComponent):
```

#### Purpose

A **two-phase component**:

1. Select a class from a dropdown
2. Configure its constructor parameters

#### Internal Flow

* Dropdown maps labels → `(Class, [ParamSpec])`
* Selecting an option:

  * Destroys old form
  * Builds a new `ParamInputComponent`
* `get_value()`:

  * Validates parameters
  * Instantiates the selected class

#### Example Output

```python
MovingAverage(period=21)
```

#### Key Design Choice

This component **does not store instances**.
It only **produces one instance at a time**.

That responsibility is delegated to `AddToListComponent`.

---

## 5️⃣ Multi-Instance Aggregation

### `gui/components/add_to_list.py`

```python
class AddToListComponent(UIComponent):
```

#### Purpose

Wraps a `SelectAndConfigure` component and allows **adding multiple configured objects**.

#### Internal State

* `_items`: List of constructed objects
* `_listbox`: Visual representation
* `_add_btn`: Enabled/disabled dynamically

#### Behavior

* Add button is enabled only when:

  * A selection exists
  * Input is valid
* Clicking **Add**:

  * Instantiates object
  * Appends to `_items`
  * Displays summary string

#### Output

```python
[
  MovingAverage(period=21),
  VWAP(days=7),
  McGinleyDynamic(period=14)
]
```

#### Why this exists

Allows:

* Multiple indicators
* Multiple strategies
* No artificial limitation to one config

---

## 6️⃣ Collapsible Containers

### `gui/components/collapsible_panel.py`

```python
class CollapsiblePanel(UIComponent):
```

#### Purpose

Wraps another `UIComponent` and provides **expand / collapse behavior**.

#### Behavior

* Header button toggles visibility
* Child component is built once
* `get_value()` returns:

  * `None` if collapsed
  * Child value if expanded

#### Usage

Primarily used for:

* Optional configuration blocks
* Reducing UI clutter

---

## 7️⃣ Chart Rendering

### `gui/components/stock_chart.py`

```python
class StockChartComponent(UIComponent):
```

#### Purpose

Render **one ticker → one Matplotlib chart**.

#### Responsibilities

* Candlestick drawing
* Indicator overlays
* Strategy signal markers
* Dual Y-axis handling
* Safe redraws

#### Important Technical Constraints

* Exactly **one Figure per instance**
* Axes are cleared, not recreated
* Secondary axis explicitly removed and rebuilt

#### Why this matters

Prevents:

* Matplotlib memory leaks
* `figure.max_open_warning`
* UI degradation over time

---

## 8️⃣ Multi-Chart Container

### `gui/components/market_chart_view.py`

```python
class MarketChartView(UIComponent):
```

#### Purpose

Manage **multiple StockChartComponent instances**, one per ticker.

#### Internal Structure

* Scrollable `Canvas`
* Inner `Frame` that holds charts
* Dictionary: `ticker → StockChartComponent`

#### API

* `clear()`:

  * Destroys all child charts
* `append_data(ticker, df)`:

  * Creates a new chart
  * Packs it into the scrollable area
  * Sets data

#### Why this design

* One chart per ticker scales better than multiplexing
* Allows lazy addition
* Enables vertical scrolling for large batches

---

## 9️⃣ Layout System (Backbone)

### `gui/layout/base/base_layout_container.py`

```python
class LayoutContainer(ABC):
```

#### Purpose

Defines a **non-visual container** for structuring UI.

Key idea:

> Layouts don’t produce values — they arrange components.

---

### `gui/layout/column.py`

```python
class Column(LayoutContainer):
```

#### Purpose

Arrange children **vertically or horizontally**, depending on packing strategy.

#### Key Behavior

* Calls `build()` on children
* Packs each child’s widget
* Applies consistent spacing

#### Design Choice

Children can be:

* `UIComponent`
* Another `LayoutContainer`

This enables **nested layouts**.

---

### `gui/layout/row.py`

```python
class Row(LayoutContainer):
```

#### Purpose

Arrange children **side-by-side horizontally**.

Used for:

* Two-column layouts
* Control vs visualization separation

---

### `gui/layout/panel.py`

```python
class Panel(LayoutContainer):
```

#### Purpose

A **size-constrained layout container**.

#### Features

* Fixed width / height
* `pack_propagate(False)` to prevent resizing
* Useful for:

  * Sidebars
  * Control panels

---

## 10️⃣ View Composition

### `gui/views/main_view.py`

#### Role

Pure **composition layer**:

* No logic
* No fetching
* No computation

It:

* Instantiates components
* Arranges them using layouts
* Exposes references (`ui_refs`) for actions

This separation allows:

* UI changes without touching pipeline logic
* Action logic without touching layout code

---

## 11️⃣ Renderer Entry Point

### `gui/QKRenderer.py`

#### Purpose

Application bootstrapper.

Responsibilities:

* Create Tk root
* Build layout tree
* Start event loop

# GUI Base Components & Layouts Classes
This section documents the **custom UI framework layer** built on top of Tkinter.
These classes form the **foundation** that all higher-level UI logic (API selection, indicators, strategies, charts) depends on.

---

## 1️⃣ Base UI Abstractions

### `gui/components/base/base_ui_component.py`

```python
class UIComponent(ABC):
```

#### Purpose

Defines the **minimal contract** for every UI element in the system.

Every visible UI element **must**:

* Be buildable
* Expose a value (or explicitly return `None`)
* Own a root Tk widget

#### Key Fields

* `self.widget`:
  The **root Tk widget** of the component (Frame, LabelFrame, Button, etc.)
* `self.visible`:
  Logical visibility flag (used by `show()` / `hide()`)

#### Required Methods

* `build(parent)`

  * Creates all Tk widgets
  * Must assign `self.widget`
* `get_value()`

  * Returns structured data from the UI
  * Or `None` for renderer-only components

#### Optional Behavior

* `show()` / `hide()` manipulate widget stacking without destroying state

#### Why this matters

This abstraction allows:

* Components and layouts to be composed uniformly
* Layout containers to treat **components and other layouts identically**
* UI state to be read generically by the pipeline runner

---

## 2️⃣ Error Handling

### `gui/components/error.py`

```python
class InvalidInputFormat(ValueError)
```

#### Purpose

A **domain-specific exception** used when user input cannot be converted to the expected type.

#### Where used

* `ParamInputComponent`
* `SelectAndConfigure`
* `AddToListComponent`

#### Why not plain `ValueError`

Allows:

* Catching UI validation errors cleanly
* Displaying meaningful error dialogs
* Separating user errors from programmer errors

---

## 3️⃣ Parameter System

### `gui/components/param_spec.py`

```python
class ParamSpec:
```

#### Purpose

Defines a **parameter schema** for user input.

Each `ParamSpec` describes:

* Name
* Expected type
* Default value
* Whether it is optional

This decouples:

* UI layout
* Input validation
* Object construction

---

### `gui/components/param_input.py`

```python
class ParamInputComponent(UIComponent):
```

#### Purpose

Renders a **form UI** from a list of `ParamSpec` objects.

#### Responsibilities

* Render labeled input fields
* Handle default values
* Convert strings → typed Python values
* Raise `InvalidInputFormat` on failure

#### Output

```python
{
  "interval": 1,
  "from_date": "2025-01-01",
  "unit": Unit.days,
}
```

#### Why this exists

* Avoids writing custom Tkinter forms per config
* Allows strategy/indicator configs to be declared declaratively

---

## 4️⃣ Selection + Configuration

### `gui/components/select_and_configure.py`

```python
class SelectAndConfigure(UIComponent):
```

#### Purpose

A **two-phase component**:

1. Select a class from a dropdown
2. Configure its constructor parameters

#### Internal Flow

* Dropdown maps labels → `(Class, [ParamSpec])`
* Selecting an option:

  * Destroys old form
  * Builds a new `ParamInputComponent`
* `get_value()`:

  * Validates parameters
  * Instantiates the selected class

#### Example Output

```python
MovingAverage(period=21)
```

#### Key Design Choice

This component **does not store instances**.
It only **produces one instance at a time**.

That responsibility is delegated to `AddToListComponent`.

---

## 5️⃣ Multi-Instance Aggregation

### `gui/components/add_to_list.py`

```python
class AddToListComponent(UIComponent):
```

#### Purpose

Wraps a `SelectAndConfigure` component and allows **adding multiple configured objects**.

#### Internal State

* `_items`: List of constructed objects
* `_listbox`: Visual representation
* `_add_btn`: Enabled/disabled dynamically

#### Behavior

* Add button is enabled only when:

  * A selection exists
  * Input is valid
* Clicking **Add**:

  * Instantiates object
  * Appends to `_items`
  * Displays summary string

#### Output

```python
[
  MovingAverage(period=21),
  VWAP(days=7),
  McGinleyDynamic(period=14)
]
```

#### Why this exists

Allows:

* Multiple indicators
* Multiple strategies
* No artificial limitation to one config

---

## 6️⃣ Collapsible Containers

### `gui/components/collapsible_panel.py`

```python
class CollapsiblePanel(UIComponent):
```

#### Purpose

Wraps another `UIComponent` and provides **expand / collapse behavior**.

#### Behavior

* Header button toggles visibility
* Child component is built once
* `get_value()` returns:

  * `None` if collapsed
  * Child value if expanded

#### Usage

Primarily used for:

* Optional configuration blocks
* Reducing UI clutter

---

## 7️⃣ Chart Rendering

### `gui/components/stock_chart.py`

```python
class StockChartComponent(UIComponent):
```

#### Purpose

Render **one ticker → one Matplotlib chart**.

#### Responsibilities

* Candlestick drawing
* Indicator overlays
* Strategy signal markers
* Dual Y-axis handling
* Safe redraws

#### Important Technical Constraints

* Exactly **one Figure per instance**
* Axes are cleared, not recreated
* Secondary axis explicitly removed and rebuilt

#### Why this matters

Prevents:

* Matplotlib memory leaks
* `figure.max_open_warning`
* UI degradation over time

---

## 8️⃣ Multi-Chart Container

### `gui/components/market_chart_view.py`

```python
class MarketChartView(UIComponent):
```

#### Purpose

Manage **multiple StockChartComponent instances**, one per ticker.

#### Internal Structure

* Scrollable `Canvas`
* Inner `Frame` that holds charts
* Dictionary: `ticker → StockChartComponent`

#### API

* `clear()`:

  * Destroys all child charts
* `append_data(ticker, df)`:

  * Creates a new chart
  * Packs it into the scrollable area
  * Sets data

#### Why this design

* One chart per ticker scales better than multiplexing
* Allows lazy addition
* Enables vertical scrolling for large batches

---

## 9️⃣ Layout System (Backbone)

### `gui/layout/base/base_layout_container.py`

```python
class LayoutContainer(ABC):
```

#### Purpose

Defines a **non-visual container** for structuring UI.

Key idea:

> Layouts don’t produce values — they arrange components.

---

### `gui/layout/column.py`

```python
class Column(LayoutContainer):
```

#### Purpose

Arrange children **vertically or horizontally**, depending on packing strategy.

#### Key Behavior

* Calls `build()` on children
* Packs each child’s widget
* Applies consistent spacing

#### Design Choice

Children can be:

* `UIComponent`
* Another `LayoutContainer`

This enables **nested layouts**.

---

### `gui/layout/row.py`

```python
class Row(LayoutContainer):
```

#### Purpose

Arrange children **side-by-side horizontally**.

Used for:

* Two-column layouts
* Control vs visualization separation

---

### `gui/layout/panel.py`

```python
class Panel(LayoutContainer):
```

#### Purpose

A **size-constrained layout container**.

#### Features

* Fixed width / height
* `pack_propagate(False)` to prevent resizing
* Useful for:

  * Sidebars
  * Control panels

---

## 10️⃣ View Composition

### `gui/views/main_view.py`

#### Role

Pure **composition layer**:

* No logic
* No fetching
* No computation

It:

* Instantiates components
* Arranges them using layouts
* Exposes references (`ui_refs`) for actions

This separation allows:

* UI changes without touching pipeline logic
* Action logic without touching layout code

---

## 11️⃣ Renderer Entry Point

### `gui/QKRenderer.py`

#### Purpose

Application bootstrapper.

Responsibilities:

* Create Tk root
* Build layout tree
* Start event loop

---

## Summary (Technical)

What you built here is **not “just Tkinter UI”** — it is:

* A component system
* A declarative configuration system
* A layout abstraction layer
* A multi-instance renderer pipeline
* A memory-safe Matplotlib embedding strategy

All of this without:

* External UI frameworks
* MVC boilerplate
* Reactive libraries

